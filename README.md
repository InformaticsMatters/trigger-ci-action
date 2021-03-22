# Trigger CI Action
A container-based GitHub Action that triggers execution of a remote CI process.
This can be used to chain CI builds that might exist in disperate repositories.
The action essentially alloys the build process in repository
**"A"** to trigger a named CI workflow in repository **"B"**.

The Trigger CI action supports the following CI (trigger) types: -

-   **GitHub Workflow Dispatch** (`ci-type: github-workflow-dispatch`)

## Inputs

### `ci-type`
**Optional** The CI type. At the moment we support the following remote CI
types: -

- github-workflow-dispatch

### `ci-owner`
**Required** The repository owner, i.e. `informaticsmatters` if the
remote CI repository is `informaticsmatters/squonk`

### `ci-repository`
**Required** The repository name, i.e. `squonk` if the
remote CI repository is `informaticsmatters/squonk`

### `ci-ref`
**Optional** The repository reference to trigger.
It's the fully qualified remote reference, a branch or a tag. Default is
`refs/heads/main`, but can be a branch, i.e. `refs/heads/dev-branch`
or a tag, i.e. `refs/tags/2021.3`, or any valid reference.

### `ci-user`
**Required**  A user that can access the remote repository

### `ci-user-token`
**Required**  The repository user's access token

### `ci-name`
**Required**  The name of the remote CI process, for **GitHub Workflow Dispatch**
types this will be the `name` assigned to the workflow you're running, which is
the `name` defined in the workflow file, _not_ the workflow file name.

### `ci-inputs`
**Optional**  The remote repository's build inputs/arguments. If used,
it sets build arguments and values in the remote CI process.
For **GitHub Workflow Dispatch** types these are the _workflow inputs_.
The inputs are declared here using a space-separated set of names and values, 
i.e. `target_input_1=xyx target_input_2=abc`.

## Example usage
In this first example we trigger the default type of workflow
(a **GitHub Workflow Dispatch** workflow) on the branch `dev-branch`
(`refs/heads/dev-branch`) of the repository `informaticsmatters/squonk`.
The workflow name being executed is `build main`.

Every trigger needs a user (and user token) that can activate the remote CI
process.

```yaml
- name: Trigger squonk
  uses: informaticsmatters/trigger-ci-action@v1
  with:
    ci-owner: informaticsmatters
    ci-repository: squonk
    ci-ref: refs/heads/dev-branch
    ci-name: build main
    ci-user: dlister
    ci-user-token: 00000000
```

---
