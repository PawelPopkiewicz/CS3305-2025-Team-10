# Useful shell commands used in development

## Processing routes.txt

```bash
grep -E -oh "^[^,]*,[^,]*,2[0-2][0-9][^,]?" routes.txt | sed "s/,777802[0-1]//g" > route_id_to_route_name.txt
```
