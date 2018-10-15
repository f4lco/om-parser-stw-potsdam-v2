.. _cache_hash:

Cache Hash
----------

The JSON endpoint requires a query parameter named ``cHash`` (short for cache hash).
It origins from TYPO and asserts that the other query parameters still have their predefined value.
The problem solved is the following: imagine a view that is subject to caching and takes a single parameter, say a blog entry ID, which sets the output of the entire view fixed.
A malicious client could start enumerating that ID, and for every possible outcome (found blog entry, 404 pages, other behaviours), one cache entry is created.
In order to prevent excessive memory consumption,  TYPO ships a hash of the parameters in order to turn down "guessed" parameters up front.

The value of ``cHash`` is computed as follows: ::

    md5(serialize(sort(array(super => secret, key1 => value1, key2 => value2, ...))))

Keys and values are drawn from the query string of the URL and restricted to a known set of "relevant" URL parameters.
The first array entry contains the server's secret - think of it as salt, of course only known to the server.

Because the hash involves a salt / secret that clients' are unable to compute, we need to obtain or hardcode these.
With greater effort, it is of course possible to extract ``cHash`` from the DOM.
However, fetching ``cHash`` does not make the parser more resilient to change. As noted, ``cHash`` is the hash of the query parameters plus some salt, effectively ``md5(secret + canteen ID)`` for our purposes. If the canteen ID changed, there is more to fix than just to account for the changed hash.

It's placing the bet on which changes first: the canteen ID or the canteen page structure. Given that extracting content from the DOM is inherently unreliable, one would have to implement the following extraction pipeline to assemble all pieces of information required to access the JSON endpoint:

1. Access the canteen selection page, this works without ``cHash``. Find canteen and extract the ``cHash`` for the canteen specific site.
2. Access canteen specific site and find the JSON endpoint URL in the DOM, containing the ``cHash`` specific to that endpoint.
3. Access the JSON endpoint to get the menu.

Given that this alternative consists of two more indirections, hard-coding ``cHash`` appears justifiable.
For this reason the automated retrieval of ``cHash`` and others is postponed until they are subject to frequent change.

