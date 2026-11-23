# c2j feature requests for recipe authors

Both features landed on c2j main. The current authoring guides show the released syntax. [Optional extension inputs](ops/EXTENSION_OPS_GUIDE.md) · [Test-only include replacements](NATIVE_RECIPE_TESTING.md)

## 1. Forward an optional recipe input to an extension op

Suppose a compression op declares an integer input `level` with a default of 6. A recipe that passes only `file` already gets level 6. The awkward case is a recipe that accepts an optional override from its own caller. Writing `level: ${{ inputs.?level.orValue(null) }}` sends an explicit null when the caller omits the override. Before optional forwarding, an author had to branch between two calls, one with the `level` line and one without.

**Suggested c2j syntax.** Allow a direct extension call to forward a CEL optional through an `optional_inputs` block:

```yaml
op: ./compress
inputs:
  file: ${{ inputs.file }}
optional_inputs:
  level: ${{ inputs.?level }}
```

Read the last line as “pass `level` if the caller supplied it.” CEL already expresses this distinction. The lookup `inputs.?level` returns an optional that records whether the key exists. CEL’s own map syntax, `{?'level': inputs.?level}`, uses that information to build either an empty map or one containing `level`. The proposed YAML block gives recipe authors the same behavior alongside ordinary inputs. [CEL optional field selection and map entries](https://pkg.go.dev/github.com/google/cel-go@v0.28.0/cel#OptionalTypes)

| Caller supplies | Key forwarded to the op | Result |
|---|---|---|
| No `level` | Key omitted | The op uses 6 |
| `level: 9` | `level: 9` | The op uses 9 |
| `level: 0` | `level: 0` | The op uses 0 |
| `level: null` | `level: null` | The integer schema reports an error |

For c2j, evaluate each entry as a CEL optional while presence is still available. If `hasValue()` is true, insert `value()` under that key. Otherwise leave the key out. Then apply the extension’s usual defaults and validation. Report a non-optional expression or a key declared in both input blocks as a recipe error.

## 2. Allow multiple recipe include mock replacements in one native test

Let a test declare a set of replacements, each targeting an authored `include` call site in the parent recipe. Each site can have its own sequence of responses. The parent evaluates the real inputs and follows its real transitions. Other includes run normally.

For example, a release recipe retries a package check while it is pending, then publishes when it is ready. A single test could mock both includes:

| Include site | First visit | Second visit |
|---|---|---|
| `check_package` | Return `{"ready":false}` | Return `{"ready":true}` |
| `publish_package` | Return `{"version":"1.2.0"}` | No second call expected |

The test can assert that the parent called `check_package` twice and then called `publish_package` once with the expected package. Two sites that include the same recipe can have different replacements.

Scope replacements to the test case. Support returned outputs, fixture artifacts and simulated include failures. Record each call’s evaluated inputs and artifact references. Report an unknown target, an unexpected extra call, an unused required response or an output that violates a declared interface.
