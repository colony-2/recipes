// This Recipes-owned test is placed temporarily in a published Cortex checkout.
// It reuses its SQLite setup, then supplies the COMPLETE evaluated producer form.
package cortex

import (
	"encoding/json"
	"io"
	"os"
	"testing"

	"github.com/colony-2/c2j/pkg/input"
	"github.com/colony-2/jobdb/pkg/jobdb"
	"github.com/stretchr/testify/require"
)

func TestRecipesGeneratedNativeSchemas(t *testing.T) {
	data, err := os.ReadFile(os.Getenv("ADAPTIVE3_REVIEW_FORMS"))
	require.NoError(t, err)
	var forms []input.InputForm
	require.NoError(t, json.Unmarshal(data, &forms))
	require.NotEmpty(t, forms)
	var vectors struct {
		Feedback []struct {
			Text       string `json:"text"`
			Meaningful bool   `json:"meaningful"`
		} `json:"feedback"`
		Scalars []struct {
			Form     input.InputForm `json:"form"`
			Response map[string]any  `json:"response"`
			Valid    bool            `json:"valid"`
		} `json:"scalars"`
	}
	data, err = os.ReadFile(os.Getenv("ADAPTIVE3_NATIVE_VECTORS"))
	require.NoError(t, err)
	require.NoError(t, json.Unmarshal(data, &vectors))
	for _, producer := range forms {
		var declaration struct {
			Directions []struct {
				ID      string `json:"id"`
				Mode    string `json:"feedback_mode"`
				Uploads bool   `json:"allow_attachments"`
			} `json:"directions"`
		}
		raw, err := json.Marshal(producer.Request)
		require.NoError(t, err)
		require.NoError(t, json.Unmarshal(raw, &declaration))
		for _, direction := range declaration.Directions {
			trials := []struct {
				name, text string
				files      bool
				valid      bool
			}{
				{"empty", "", false, direction.Mode == "forbidden"},
				{"whitespace", " \u0085\ufeff", false, false},
				{"unicode", "  日本語 🙂\n", false, direction.Mode == "required"},
				{"uploads", "", true, direction.Uploads},
			}
			if direction.Mode == "optional" {
				for i := range trials {
					trials[i].valid = !trials[i].files || direction.Uploads
				}
			}
			for _, vector := range vectors.Feedback {
				trials = append(trials, struct {
					name, text string
					files      bool
					valid      bool
				}{"shared-feedback", vector.Text, false, direction.Mode == "optional" || direction.Mode == "required" && vector.Meaningful || direction.Mode == "forbidden" && vector.Text == ""})
			}
			for _, trial := range trials {
				t.Run(producer.Title+"/"+direction.ID+"/"+trial.name, func(t *testing.T) {
					s, ctx, form := nativeReviewV2(t, func(f *input.InputForm) {
						*f = producer
						if f.RequestID == "" {
							f.RequestID = "generated-native"
						}
					})
					var files []any = []any{}
					if trial.files {
						files = []any{jobdb.NewArtifactFromBytes("contributions/0/notes.md", []byte("first note")), jobdb.NewArtifactFromBytes("contributions/1/notes.md", []byte("second note"))}
					}
					response := map[string]any{"direction": direction.ID, "feedback": trial.text, "attachments": files, "settings": map[string]any{}}
					out, err := s.inputs.SubmitStructuredResponse(ctx, "tenant", "job", input.StructuredSubmission{RequestID: form.RequestID, SubmissionID: "generated", Response: response}, input.Actor{ID: "recipes-native", Kind: "test"})
					if !trial.valid {
						require.ErrorContains(t, err, "response")
						require.Nil(t, out.Receipt)
						_, pendingErr := s.inputs.GetForm(ctx, "tenant", "job")
						require.NoError(t, pendingErr)
						return
					}
					require.NoError(t, err)
					require.Equal(t, form.RequestID, out.Receipt.RequestID)
					accepted := out.Response.(map[string]any)
					require.Equal(t, trial.text, accepted["feedback"])
					if trial.files {
						attachments := accepted["attachments"].([]any)
						require.Len(t, attachments, 2)
						names := map[string]bool{}
						for i, value := range attachments {
							ref := value.(map[string]any)
							keyData, e := json.Marshal(ref["stored"].(map[string]any)["key"])
							require.NoError(t, e)
							var key jobdb.ArtifactKey
							require.NoError(t, json.Unmarshal(keyData, &key))
							require.False(t, names[key.Name])
							names[key.Name] = true
							artifact, e := s.engine.GetArtifact("tenant", key)
							require.NoError(t, e)
							reader, e := artifact.Open()
							require.NoError(t, e)
							bytes, e := io.ReadAll(reader)
							require.NoError(t, e)
							require.NoError(t, reader.Close())
							require.Equal(t, []string{"first note", "second note"}[i], string(bytes))
						}
					}
				})
			}
		}
	}
	for _, vector := range vectors.Scalars {
		s, ctx, form := nativeReviewV2(t, func(f *input.InputForm) { *f = vector.Form; f.RequestID = "scalar-native" })
		out, err := s.inputs.SubmitStructuredResponse(ctx, "tenant", "job", input.StructuredSubmission{RequestID: form.RequestID, SubmissionID: "scalar", Response: vector.Response}, input.Actor{ID: "recipes-native", Kind: "test"})
		if vector.Valid {
			require.NoError(t, err)
			require.NotNil(t, out.Receipt)
		} else {
			require.ErrorContains(t, err, "response")
			require.Nil(t, out.Receipt)
		}
	}
}
