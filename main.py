# {
#     search(query: "stars:>0", type: REPOSITORY, first: 5) {
#         pageInfo {
#             endCursor
#         }
#         edges {
#             node {
#                 ... on Repository {
#                     createdAt
#                     stargazerCount
#                     pullRequests(states: [MERGED, CLOSED]) {
#                         totalCount
#                     }
#                     nameWithOwner
#                     sshUrl
#                 }
#             }
#         }
#     }
# }
