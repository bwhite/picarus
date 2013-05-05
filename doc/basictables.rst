Basic Tables
============
Tables that are a small constant size are stored in memory on the REST servers.

Parameters
-----------

Row
^^^
Corresponds to a model/factory that can be instantiated using POST /data/models.  

Permissions
^^^^^^^^^^^
Users can read all columns but not write to any.

Columns
^^^^^^^^^^^^^^^^

+--------------+------------------------------------------------------------------------------------------------------+
| Column       | Description                                                                                          |
+--------------+------------------------------------------------------------------------------------------------------+
| type         | Either model (i.e., directly create model) or factory (i.e., process input data and create model)    |
+--------------+------------------------------------------------------------------------------------------------------+
| name         | Name of the model (also corresponds to the picarus_takeout class) or factory                         |
+--------------+------------------------------------------------------------------------------------------------------+
| kind         | Category of model such as classifier/feature  (solely used for categorization in the web app)        |
+--------------+------------------------------------------------------------------------------------------------------+
| input_type   | Input type to the model, defines a specific binary encoding                                          |
+--------------+------------------------------------------------------------------------------------------------------+
| output_type  | Output type from the model, defines a specific binary encoding                                       |
+--------------+------------------------------------------------------------------------------------------------------+
| params       | JSON object, keys are parameter names, values are object with type and constraints for that type     |
+--------------+------------------------------------------------------------------------------------------------------+
| input_types  | Used by factories to specify what input types they require (e.g., feature and meta for svmlinear)    |
+--------------+------------------------------------------------------------------------------------------------------+
