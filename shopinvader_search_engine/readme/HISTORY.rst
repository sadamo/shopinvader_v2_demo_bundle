16.0.1.0.1 (2023-10-13)
~~~~~~~~~~~~~~~~~~~~~~~

**Features**

- A complete refactoring has been done to the code. This refactoring was driven by
  the following goals:

  * Make the code more readable and maintainable.
  * Put in place a way to validate data exported to the indexes
  * Ease the work of frontend developers by providing a schema for the data
    exported to the indexes.

  Some technical choices have been made to achieve these goals:

  * We removed the need to force the developer to define a specific binding model
    for each model that needs to be indexed.
  * We defined serializers based on Pydantic models. This choice allows you to
    validate the data, generate the documentation and the schema of the data
    exported to the indexes. It also makes the serialization mechanism more
    explicit and easier to understand.
  * We defined more fine-grained modules.

  If you need to add additional information to the data exported to the indexes,
  you only need to extends the Pydantic models by adding your additional fields
  and extending the method initializing the model from an odoo record. (`#1390 <https://github.com/shopinvader/odoo-shopinvader/issues/1390>`_)


**Misc**

- `#1423 <https://github.com/shopinvader/odoo-shopinvader/issues/1423>`_


10.0.1.0.0 (2017-04-11)
~~~~~~~~~~~~~~~~~~~~~~~

* First real version : [REF] rename project to the real name : shoptor is dead long live to shopinvader", 2017-04-11)

12.0.1.0.0 (2019-05-21)
~~~~~~~~~~~~~~~~~~~~~~~

* [12.0][MIG] shopinvader_search_engine
