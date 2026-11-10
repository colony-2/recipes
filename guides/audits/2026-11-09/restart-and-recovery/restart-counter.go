package main

import (
	"encoding/json"
	"fmt"
	"github.com/colony-2/c2j/pkg/contextual"
	"github.com/colony-2/c2j/pkg/recipe"
	"github.com/colony-2/c2j/pkg/template"
)

func must(e error) {
	if e != nil {
		panic(e)
	}
}
func main() {
	root, e := template.NewRecipeResolutionContext(&contextual.GitCommitContext{}, nil, contextual.JobContext{})
	must(e)
	resolved, e := root.ResolveCompositeInputs(map[string]interface{}{"prior_rebase_repairs": "${{ inputs.?prior_rebase_repairs.orValue(0) }}"})
	must(e)
	fmt.Printf("recipe default: %T(%v)\n", resolved["prior_rebase_repairs"], resolved["prior_rebase_repairs"])
	sm, e := root.NewChildContext(template.ScopeStateMachine, recipe.NodeMetadata{ID: "develop"}, "", resolved)
	must(e)
	expr := "${{ inputs.prior_rebase_repairs + (state_exists('rebase_repair') ? size(states.rebase_repair.runs) + 1 : 0) }}"
	show := func(label string) {
		v, e := sm.ResolveMap(map[string]interface{}{"value": "${{ inputs.prior_rebase_repairs }}"})
		must(e)
		fmt.Printf("%s Go value: %T(%v)\n", label, v["value"], v["value"])
		out, e := sm.ResolveMap(map[string]interface{}{"counter": expr})
		fmt.Printf("%s unchanged expression: %v; error=%v\n", label, out, e)
	}
	show("initial")
	show("repeat without restart")
	op, e := sm.NewChildContext(template.ScopeOp, recipe.NodeMetadata{ID: "merge_reviewed_candidate"}, "", nil)
	must(e)
	clone, e := op.CloneForRestart()
	must(e)
	op.AdoptRestart(clone)
	show("after native restart clone/adopt")
	// Control: Go preserves concrete field types; interface-valued maps are different.
	typed := struct {
		Counter int64 `json:"counter"`
	}{Counter: 0}
	b, e := json.Marshal(typed)
	must(e)
	var same struct {
		Counter int64 `json:"counter"`
	}
	must(json.Unmarshal(b, &same))
	var dynamic map[string]interface{}
	must(json.Unmarshal(b, &dynamic))
	fmt.Printf("JSON control: typed field=%T; interface map value=%T\n", same.Counter, dynamic["counter"])
}
