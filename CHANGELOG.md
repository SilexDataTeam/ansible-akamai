# Silexdata Akamai Release Notes

**Topics**

- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#deprecated-features">Deprecated Features</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#minor-changes-1">Minor Changes</a>

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="release-summary"></a>
### Release Summary

This release adds a test and CI pipeline for the collection and hardens the
<code>manage\_akamai</code> module\: check mode support\, graceful handling of missing
Python dependencies\, stricter input validation\, and documentation and
packaging\-standards fixes\.

<a id="minor-changes"></a>
### Minor Changes

* manage\_akamai \- add check mode support\; no API calls are made in check mode and a change is predicted only for write methods \(PATCH\, POST\, PUT\)\.
* manage\_akamai \- document the <code>edge\_auth</code> suboptions and correct the documented <code>edge\_config</code> type to <code>path</code>\.
* manage\_akamai \- validate the <code>method</code> parameter against its supported choices \(GET\, PATCH\, POST\, PUT\)\.

<a id="deprecated-features"></a>
### Deprecated Features

* manage\_akamai \- the old module name <code>silexdata\.akamai\.akamai</code> is deprecated in favor of <code>silexdata\.akamai\.manage\_akamai</code> and will be removed in 2\.0\.0\; a redirect keeps it working with a deprecation warning\.

<a id="bugfixes"></a>
### Bugfixes

* manage\_akamai \- fail with a clear <code>missing required library</code> message when <code>requests</code> or <code>edgegrid\-python</code> is not installed\, instead of raising an import error or printing to stdout\.
* manage\_akamai \- guard the optional third\-party imports so the module can be imported \(and its documentation collected\) without <code>requests</code> or <code>edgegrid\-python</code> present\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary-1"></a>
### Release Summary

Initial release of the silexdata\.akamai Ansible Collection\.

<a id="minor-changes-1"></a>
### Minor Changes

* Add the akamai plugin for managing Akamai resources\.
* Standardize the repository structure
