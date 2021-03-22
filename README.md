# Trigger CI Action
A GitHub Action that triggers execution of a remote CI process. This can be
used to chain CI builds that exist in separate repositories, so repository
**a** can trigger a CI workflow in repository **b**.

The Trigger CI action supports the following trigger-types: -

-   GitHub Workflow Dispatch (`ci-type: github-workflow-dispatch`)

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
    description: The repository user's token

### `ci-user-token`
**Required**  The repository user's access token

### `ci-name`
**Required**  The name of the remote CI process, for **GitHub Workflow Dispatch**
types this will bne the `name` assigned to the workflow you're running. Its
name, _not_ it's file name.

### `ci-inputs`
**Optional**  The remote repository's inputs. This is optional and, if used,
sets inout keys and values in the remote build. For **GitHub Workflow Dispatch**
types this will be a space-separated set of input names and values, 
i.e. `target_input_1=xyx target_inoput_2=abc`.

## Example usage
Here we trigger the default type of workflow (a GitHub Workflow Dispatch
workflow) on the branch `dev-branch` (`refs/heads/dev-branch`) of the
repository `informaticsmatters/squonk`. the workflow name here is `build main`.

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
