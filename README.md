## General info

This app analyze pdf document and store unique documents data (some doc attributes and unique links).
Provide API for interactions and Swagger Docs.



## Assumptions:

1. Document data without urls would be stored
2. Different pdf documents could contain same urls
3. Stored only unique urls; Unique urls has unique addresses
4. Stored only unique pdf documents; Unique pdf document - has unique file size with filename. - So for this i must store sha256sum for every unique doc. Of course we could think that documents could be only unique by file name or file name and size - but it possible that could be a document clone but with another content (with same name and size)
5. Stored document name with extension
6. Alive urls - which return status code less than 400 response status code
7. Alive urls check only with optional request type

## TODO: 

1. Add client page for upload pdf document
2. Need use Celery because of long time pdf parsing and verify urls
3. Upgrade check url alive status - in reason of block some services of crawling
