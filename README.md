# Parse, don't validate

I have never been happy with validation code I wrote, I found [this blog post](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/) and wanted to explore the idea.

We want to guarantee our data is valid so downstream systems don't have to duplicate the validation step. To do this we need to guarantee type safety and avoid null values in our fields. 

The implementation has 3 classes `MetadataParser`, `UpdateField`, and `Metadata`.

The magic comes from creating the class `UpdateField` that describes our "update" action. This allows us to only change values in the `Metadata` object when they are valid, otherwise we flag the update with an error, and it never occurs.
