# Notes for how to connect frontend to backend

* Show all available components in the sidebar

## Events:

### Add a component (GridWidget -> dropEvent)
* call addComponent on the logic controller
* Create a GridWidget with the right amount of inputs and outputs, including their "labels" (can be derived from the dict keys)
* The order of inputs and outputs should be right

### Create a connection (GridWidget -> mouseReleaseEvent -> if draggingLine)
* call addConnection on the logic controller
  * four parameters: origin, originKey, target, targetKey
* Only create the connection if addConnection returns True

### Remove connection (GridWidget -> removeConnectionTo)
* call removeConnection on the logic controller
  * parameters: same as createConnection

### Remove LogicComponent (GridItem -> deleteItem (maybe move to GridWidget))
* call removeComponent (Luis makes sure the connections are removed in the backend)
  * pass reference to component
* make sure all connections are also removed in the frontend
