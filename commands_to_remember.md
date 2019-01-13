# Commands to Remember

The purpose of this doc is to contain one-off commands worth remembering for various reasons. Do your best to organize via applicability.

## DigitalOcean

  * List all slugs, pipe to jq for parsing

`curl -X GET -q -H "Content-Type: application/json" -H "Authorization: Bearer $DIGITALOCEAN_API_KEY" "https://api.digitalocean.com/v2/images?per_page=100" | jq '.images[].slug | values'`
