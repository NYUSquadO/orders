# Orders

[![Build Status](https://github.com/NYUSquadO/orders/actions/workflows/tdd.yml/badge.svg)](https://github.com/NYUSquadO/orders/actions/workflows/tdd.yml)
[![Build Status](https://github.com/NYUSquadO/orders/actions/workflows/bdd.yml/badge.svg)](https://github.com/NYUSquadO/orders/actions/workflows/bdd.yml)
[![codecov](https://codecov.io/gh/NYUSquadO/orders/branch/main/graph/badge.svg?token=95UV2GZXFD)](https://codecov.io/gh/NYUSquadO/orders)

DevOps homework project for CSCI-GA.2820-001 DevOps and Agile Methodologies Fall 2021.
This is a back end for an eCommerce web site as a RESTful services for a client to operate on orders.

## Introduction

The service code is contained in `routes.py` while the business logic for manipulating Orders is in the `models.py` file. This follows the popular Model View Controller (MVC) separation of duities by keeping the model separate from the controller. As such, we have two tests suites: one for the model (`test_models.py`) and one for the serveice itself (`test_routes.py`)

## Prerequisite Installation using Vagrant

This project requires Vagrant and VirtualBox. Those are the things that are needed to download before you run the code. You should download Docker Desktop instead of VirtualBox if you use an 2020 Apple Mac with the M1 chip.

Download: [Vagrant](https://www.vagrantup.com/)

Intel Download: [VirtualBox](https://www.virtualbox.org/)

Apple M1 Download: [Apple M1 Tech Preview](https://docs.docker.com/docker-for-mac/apple-m1/)

### Using Vagrant and VirtualBox

```shell
git clone https://github.com/NYUSquadO/orders.git
cd orders
vagrant up
```

### Using Vagrant and Docker Desktop

For users that use Docker as a provider instead of VirtualBox, this is useful for owners of Apple M1 Silicon Macs which cannot run VirtualBox because they have a CPU based on ARM architecture instead of Intel.

Just add `--provider docker` to the `vagrant up` command like this:

```sh
git clone https://github.com/NYUSquadO/orders.git
cd orders
vagrant up --provider docker
```

## Running the tests

You can now `ssh` into the virtual machine and run the service and the test suite:

```sh
vagrant ssh
cd /vagrant
```

You will now be inside the Linux virtual machine so all commands will be Linux commands.

## Manually running the Tests
This repository has both unit tests and integration tests. You can now run `nosetests` and `behave` to run the TDD and BDD tests respectively.

### Test Driven Development (TDD)
Run the tests using `nosetests`

```shell
$ nosetests
```
If you want to check what lines of code that were not tested use:

```shell
$ coverage report -m
```

 If you use programming editors like VS Code, it's useful that you install plug-ins that will use `pylint` while you are editing. This help you catch a lot of errors while you code. It's always helpful to code with pylint active.

### Behavior Driven Development (BDD)

These tests require the service to be running becasue unlike the the TDD unit tests that test the code locally, these BDD intagration tests are using Selenium to manipulate a web page on a running server.

Run the tests using `behave`

```sh
honcho start &
behave
```

Note that the `&` runs the server in the background. To stop the server, you must bring it to the foreground and then press `Ctrl+C`

Stop the server with

```sh
fg
<Ctrl+C>
```
## Exit the Virtual Machine

When you are done, you can exit and shut down the vm with:

```shell
$ exit
$ vagrant halt
```

If the VM is no longer needed you can remove it with:

```shell
$ vagrant destroy
```

## What's featured in the project?

    * ./service/routes.py -- the main Service routes using Python Flask
    * ./service/models.py -- the data model using SQLAlchemy
    * ./service/error_handlers.py -- these error handlers send back json
    * ./tests/test_routes.py -- test cases against the Order service
    * ./tests/test_models.py -- test cases against the Order model
    * ./features/orders.feature -- Behave feature file
    * ./features/steps/steps.py -- Behave step definitions

| Endpoint       |    Method  | Path          |                      Description
|----------------|-------|-------------|     -------------------------
| index        |      GET    |  /          |  Index
| create_order | POST   |   /orders  |  Create an order based on the data in the body that is posted  
| list_orders   |  GET     |  /orders            |             Return all of the Orders
| get_order    | GET    |  /orders/\<int:order_id>       |   Retrieve a single Order
| update_order | PUT     | /orders/\<int:order_id>      |   Update an Order based on the body that is posted
| delete_order   |   DELETE | /orders/\<int:order_id>   |    Delete an Order based on the id specified in the path
| add_item   |   POST | /orders/\<int:order_id>/items   |   Add item to existing order based on the data in the body that is posted 
| get_items_in_order    | GET    |  /orders/\<int:order_id>/items       |   Retrieve order items
| read_item    | GET    |  /orders/\<int:order_id>/items/\<int:item_id>       |   Retrieve a single Order Item
| update_order_item | PUT     | /orders/\<int:order_id>/items/\<int:item_id>      |   Update an Order Item based on the body that is posted
| delete_item   |   DELETE | /orders/\<int:order_id>/items/\<int:item_id>   |    Delete item in order based on the item id and order id specified in the path
| list_orders   |   GET  | /orders?cust_id=<customer_id>   |    Query for orders by customer ID
| list_orders   |   GET  | /orders?item_id=<item_id>   |    Query for orders by item ID
| cancel_orders   |  PUT  | /orders/<int:order_id>/cancel   |  Cancel Order
| delete_item   |   DELETE | /orders/\<int:order_id>/items/\<int:item_id>   |    Delete item in order based on the item id and order id specified in the path

# IBM Cloud Foundry URL
DEV: https://nyu-order-service-fall2101.us-south.cf.appdomain.cloud/

PROD: https://nyu-order-service-fall2101-prod.us-south.cf.appdomain.cloud/
