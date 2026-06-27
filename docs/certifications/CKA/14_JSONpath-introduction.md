# 14.1 - Introduction to JSONPath

## 14.1 - Introduction to YAML

- Ansible playbooks format similar to XML and JSON
- Used to express data
- Data in YAML files, at its most basic form is a series of Key-Value pairs, separated by a colon
- For an array:

```yaml
- entry1: value1
- entry2: value2
- entry3: value3
```

- For a dictionary:

```yaml
item:
  property1: value1
  property2: value2
```

- **Note:** 2 spaces determine what properties come under what iteM
- Can have lists containing dictionaries containing lists
- To store information about different properties of a single item, use a dictionary
- If the properties need further segregation, can use dictionaries within dictionary items
- For multiple items of the same type, use an array
- To store information for multiple items, expand each array item to a the dictionary for each

- **Key Notes:**
  - Dictionary = Unordered
  - Lists / Arrays = Ordered
  - Comments added via #

## 14.2 - Introduction to JSONpath

- **Yaml vs Json:**
  - Data can be expressed via both
  - To segregate data, methods differ:
    - YAML - Indentations and -'s
    - JSON - Indentation and {} for dictionaries, [] for array items
- JSON data can be queried via JSON Path
- To select an item, specify it as `<item>`
- For a dictionary property: `<item>.<property>`
- **Note:** Anything within { } denotes a dictionary
- The top-level dictionary, which isn't named, is denoted by a $
- A typical query is `$.item.property` etc
- Any output from a JSONpath query is an array []
- To query an array/list, use square brackets to reference the position, with positions starting at `[0]`.
  - E.g. 1st element: `$.[0]`
- For dictionaries in lists, combine the query use for all
- For criteria: `$.[CRITERIA]` e.g.:
  - `$.[?( @ > 40 )]`
  - In this case, ?() signals to use a filter, the @ symbol signifies "each item"
  - Queries could be used to accommodate for changing positions
  - E.g. `$.car.wheels[?(@.location == "rear-right")].model`
    - Only entries that satisfy the citeria "location = rear-right" will be returned.

## 14.3 - JSONPath: Wildcard

- Denoted by `*`, meaning "any", can be used to retrieve all/any properties of a
particular dictionary
- Can swap `*` as a value when referencing an array position i.e. `[*]`

## 14.4 - JSONPath: Advanced List Queries

- To get all names in an array's particular range, add `[x:y]`, where `x` is the first
element's position, `y` is the end position of the range `+1`
- To iterate over a step, insert: `[x:y:z]`, where z is the step rate
- To get the last item: `[-1:0]`

## 14.5 - Advanced Kubectl Commands: Kubectl and JSONPath

- **Prerequisites:**
  - JSONPath for beginners
  - JSONPath Practice tests - Kodekloud: General use and for Kubernetes
- Why JSON Path?
  - Large data sets involved with production-grade clusters
    - 100s of nodes
    - 1000s of PODS, Deployments, ReplicaSets etc
  - More often than not, will want to quickly print information for large numbers
of resources and particular information
- Kubectl commands invokes the APIServer, which obtains the information requested
in a JSON format and is redisplayed in a readable format by Kubectl
  - Particularly noticeable in kubectl get commands
  - For additional information, add `-o` wide flag
- **Example:**
  - Suppose we want to see the following:
    - CPU count
    - Taints and Tolerations
    - Pod name and Images
  - There is no built-in kubectl command for this, but we can use kubectl and
JSON path in combination to get the particular fields
- To use JSON Path in Kubectl, consider the 4 steps:
  1. Identify the kubectl command required e.g. kubectl get pods
  1. Familiarize yourself with the JSON format output: add the `-o` json flag
  1. From the JSON output, figure out the custom query you'd want to apply, e.g.
for container images of a particular pod: `.items[*].spec.containers[*].image`
  1. Combine the kubectl command with the JSON query i.e. `kubectl get pods
-o=jsonpath='{JSON_PATH_QUERY}'`
- **Note:**
  - For multiple queries, within the '', encompass each query by {}
  - To format this, use any of the following:
    - `{"\n"}` - New line (Add in between queries)
    - `{"\t"}` - Tab
- Looping through ranges: `'{range .items[*]} {Queries} {end}'`
- Can print custom columns via: `-o=custom-columns=<COLUMN_NAME>:<JSON PATH>, <COLUMN>:<JSON PATH>`
  - Recommended to view full query first then forming the JSON query
- Use `--sort-by` property where necessary e.g. `--sort-by=.metadata.name`
