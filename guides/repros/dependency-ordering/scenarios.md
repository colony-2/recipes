# Dependency recommendation scenarios

These fixed facts are supplied identically to each instruction variant. The model receives only its selected scenario, the common question and its instruction variant.

## reader-producer

You own A, a producer of stored records. Your request includes activating format v2 and updating B, the reader. A can add a switch while continuing to emit v1. B on main reads only v1 and needs compatible support to read both formats. Neither cell has published any v2 work. Both cells use normal published dependencies. Plan the work needed to finish this request.

## provider-adoption

You own A, an API provider. Your request includes adding an optional API operation and making B adopt it. Nothing has been edited yet. B implements the consuming client and uses released A dependencies from main. Adoption is required before this overall request finishes. Also explain what you would change if the requester instead allowed B adoption in a later request.

## consumer-upstream

You own B, which consumes A's API. You have already saved useful local feature edits. Finishing your feature requires one additive API operation from A. A's main does not provide it. The API change alone can be implemented, reviewed and published without B. Your request is to finish B's feature.

## late-provider

You own A, an API provider. You have already saved API changes and unrelated local cleanup in the same job candidate. You now discover your current request requires B to adopt the API before the overall request finishes. B uses A from published dependencies; A main lacks the API. The private candidate contains useful code for the prerequisite. Describe how existing edits and workspace state affect your next steps.

## advice-candidate

You own A and have an unpublished candidate for an optional API. Before deciding the final contract, you want B's owner to advise on compatibility. You also want an isolated disposable check of that candidate together with B; this check is not a request to deliver or merge B adoption. B normally uses A from main. Describe the next actions and what these checks would establish.

## local-only

You own A. Your request is to improve a local settings parser and its error messages. No other cell depends on this parser or needs to adopt the change. The repository has the needed code and ordinary local tests. Nothing has been edited yet. Describe your next steps.

Every scenario asks: What changes if required prerequisite work fails, is cancelled, or completes only a diagnostic without publishing the needed change? If no prerequisite exists, say so.

## Neutral reader/producer rephrasing

You act for cell A, which writes stored records; cell B reads those records. The request is to enable stored format v2 and update B’s reader. A can prepare a switch while it continues writing v1. The reader published on main supports only v1 and needs compatible support for both formats. Neither cell has published v2 changes. Normal published dependencies apply to both. Describe the delivery plan.

This restates the same facts for the extended sample; it adds no dependency on a producer library.
