# Trigger CI Action
A container-based GitHub Action that triggers execution of a remote CI process.
This can be used to chain CI builds that might exist in disperate repositories.
The action essentially allows the build process in repository
**"A"** to trigger a named CI process in repository **"B"**.

The Trigger CI action supports the triggering the following remotes CI
processes: -

-   **GitHub Workflow Dispatch** (`ci-type: github-workflow-dispatch`)

## Inputs

### `ci-type`
**Optional** The type of remote CI process to trigger.
At the moment we support the following types: -

- `github-workflow-dispatch`

### `ci-owner`
**Required** The remote repository owner, i.e. `informaticsmatters` if the
remote CI repository is `informaticsmatters/squonk`

### `ci-repository`
**Required** The repository name, i.e. `squonk` if the
remote CI repository is `informaticsmatters/squonk`

### `ci-ref`
**Optional** The repository reference to trigger.
It's the fully qualified remote reference, a branch or a tag. Default is
`refs/heads/main`, but can be a branch, i.e. `refs/heads/dev-branch`
or a tag, i.e. `refs/tags/2021.3`, or any valid reference.

For _new-style_ GitHub repositories the default will be sufficient to trigger
a build on the main branch (where the main branch is now called `main`).
For older repositories you may have to use this input and
set it to the old main name, e.g. `refs/heads/master`

### `ci-user`
**Required** A user that can access the remote repository

### `ci-user-token`
**Required** The repository user's access token

### `ci-name`
**Required** The name of the remote CI process, for **GitHub Workflow Dispatch**
types this will be the `name` assigned to the workflow you're running, which is
the `name` defined in the workflow file, _not_ the workflow file name.

### `ci-inputs`
**Optional** The remote repository's build inputs or arguments. If used,
it is used to set build arguments and values in remote CI processes that
support this mechanism. For **GitHub Workflow Dispatch** types
these will be used to set corresponding _workflow inputs_.
The inputs are declared here using a space-separated set of names and values, 
i.e. `target_input_1=xyx target_input_2=abc`, where `target_input_1` and
`target_input_2` are inputs declared in the remote workflow's
`workflow_dispatch` configuration.

>   Do not put spaces around the input's '='. The action expects
    each key and value in the form <key>=<value>.

## Example usage
In this first example we trigger the default type of workflow
(a **GitHub Workflow Dispatch** workflow) on the branch `dev-branch`
(`refs/heads/dev-branch`) of the repository `informaticsmatters/squonk`.
The workflow name being executed is `build main`.

>   Every trigger needs a user (and user token) that can activate the remote CI
    process, illustrated here using secrets available to the triggering
    repository's workflow.

```yaml
- name: Trigger squonk
  uses: informaticsmatters/trigger-ci-action@v1
  with:
    ci-owner: informaticsmatters
    ci-repository: squonk
    ci-ref: refs/heads/dev-branch
    ci-name: build main
    ci-user: ${{ secrets.SQUONK_USER }}
    ci-user-token: ${{ secrets.SQUONK_USER_TOKEN }}
```

If the remote CI process accepts inputs we can provide values for them using
the action's `ci-inputs` property by providing a space-separated set of
keys and values.

Here we provide values `xyz` and `abc` for the inputs `target_input_1` and
`target_input_2`: -

```yaml
- name: Trigger squonk with inputs
  uses: informaticsmatters/trigger-ci-action@v1
  with:
    ci-owner: informaticsmatters
    ci-repository: squonk
    ci-name: build main
    ci-inputs: >-
      target_input_1=xyx
      target_input_2=abc
    ci-user: ${{ secrets.SQUONK_USER }}
    ci-user-token: ${{ secrets.SQUONK_USER_TOKEN }}
```

---
