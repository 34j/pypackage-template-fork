#!/bin/sh
owner=$1
name=$2
repositoryId="$(gh api graphql -f query='{repository(owner:"'$owner'",name:"'$name'"){id}}' -q .data.repository.id)"
echo "Creating branch protection rule for $owner/$name"
gh api graphql -f query='
mutation($repositoryId:ID!) {
  createBranchProtectionRule(input: {
    repositoryId: $repositoryId
    pattern: "[main,master]*"
    allowsForcePushes: true
  }) { clientMutationId }
}' -f repositoryId="$repositoryId"
echo "Setting workflow permissions for $owner/$name"
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "repos/$owner/$name/actions/permissions/workflow" \
  -f default_workflow_permissions='read' \
  -F can_approve_pull_request_reviews=true
echo "Installing $owner/$name to the GitHub App"
