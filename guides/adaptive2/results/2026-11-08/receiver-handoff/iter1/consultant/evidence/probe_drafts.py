"""Read-only consultation probes against the supplied contract model."""
from drafts import Conflict, Drafts


def check(label, condition):
    assert condition, label
    print(f"PASS: {label}")


store = Drafts()
check("absent draft is empty version zero", store.read("note") == {"text": "", "version": 0})
for version, text in enumerate(("first", "second", "third", "fourth")):
    store.write("note", text, version)
check("four saves retain only current text in the model", store.values == {"note": {"text": "fourth", "version": 4}})
try:
    store.write("note", "stale overwrite", 2)
except Conflict as error:
    check("stale write reports current version", error.args == (4,))
else:
    raise AssertionError("stale write should conflict")
check("conflict leaves current state unchanged", store.read("note") == {"text": "fourth", "version": 4})
check("equal text still advances version", store.write("note", "fourth", 4) == {"text": "fourth", "version": 5})
check("explicit empty text is a successful save", store.write("note", "", 5) == {"text": "", "version": 6})

large = "é" * 32768
check("exactly 65536 UTF-8 bytes are accepted", store.write("large", large, 0)["version"] == 1)
for label, bad_text, exception in (
    ("65538 UTF-8 bytes are rejected", large + "é", ValueError),
    ("unencodable Unicode is rejected", "\ud800", UnicodeEncodeError),
):
    before = store.read("large")
    try:
        store.write("large", bad_text, before["version"])
    except exception:
        check(label, store.read("large") == before)
    else:
        raise AssertionError(label)

response = store.write("retry", "committed", 0)
try:
    store.write("retry", "committed", 0)
except Conflict as error:
    check("retry after a lost response conflicts without a second commit", error.args == (1,) and store.read("retry") == response)
else:
    raise AssertionError("retry should conflict")
check("a new model instance has no persisted state", Drafts().read("note") == {"text": "", "version": 0})
check("no history read method exists", not hasattr(store, "history"))
print("All probes passed. These results describe the pure model, not a deployed HTTP service.")
