# Orders
NYU DevOps lab on Test Driven Development for CSCI-GA.2820-001 DevOps and Agile Methodologies Fall 2021.
This is a back end for an eCommerce web site as a RESTful services for a client to operate on orders.

## Introduction

This lab introduces **Test Driven Development** using `PyUnit` and `nose` (a.k.a. `nosetests`). It also demonstrates how to create a simple RESTful service using Python Flask and PostgreSQL. The resource model is persistences using SQLAlchemy to keep the application simple. It's purpose is to show the correct API calls and return codes that should be used for a REST API.

**Note:** The service code is contained in `routes.py` while the business logic for manipulating Orders is in the `models.py` file. This follows the popular Model View Controller (MVC) separation of duities by keeping the model separate from the controller. As such, we have two tests suites: one for the model (`test_models.py`) and one for the serveice itself (`test_routes.py`)

## Prerequisite Installation using Vagrant

The easiest way to use this lab is with Vagrant and VirtualBox. If you don't have this software the first step is down download and install it. If you have an 2020 Apple Mac with the M1 chip, you should download Docker Desktop instead of VirtualBox. Here is what you need:

Download: [Vagrant](https://www.vagrantup.com/)

Intel Download: [VirtualBox](https://www.virtualbox.org/)

Apple M1 Download: [Apple M1 Tech Preview](https://docs.docker.com/docker-for-mac/apple-m1/)

Install each of those. Then all you have to do is clone this repo and invoke vagrant:

### Using Vagrant and VirtualBox

```shell
git clone https://github.com/NYUSquadO/orders.git
cd orders
vagrant up
```

### Using Vagrant and Docker Desktop

You can also use Docker as a provider instead of VirtualBox. This is useful for owners of Apple M1 Silicon Macs which cannot run VirtualBox because they have a CPU based on ARM architecture instead of Intel.

Just add `--provider docker` to the `vagrant up` command like this:

```sh
git clone https://github.com/NYUSquadO/orders.git
cd lab-flask-tdd
vagrant up --provider docker
```

This will use a Docker container instead of a Virtual Machine (VM). Everything else should be the same.

## Running the tests

You can now `ssh` into the virtual machine and run the service and the test suite:

```sh
vagrant ssh
cd /vagrant
```

You will now be inside the Linux virtual machine so all commands will be Linux commands.

## Manually running the Tests

Run the tests using `nosetests`

```shell
$ nosetests
```
You can see a percentage of coverage report at the end of your tests. If you want to see what lines of code were not tested use:

```shell
$ coverage report -m
```

 If you use programming editors like VS Code, it's useful that you install plug-ins that will use `pylint` while you are editing. This help you catch a lot of errors while you code. It's always helpful to code with pylint active.

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

    * app/routes.py -- the main Service routes using Python Flask
    * app/models.py -- the data model using SQLAlchemy
    * tests/test_routes.py -- test cases against the Order service
    * tests/test_models.py -- test cases against the Order model

| Endpoint       |    Method  | Path          |                      Description
|----------------|-------|-------------|     -------------------------
| index        |      GET    |  /          |  Index
| create_order | POST   |   /orders  |  Create an order based on the data in the body that is posted  
| list_orders   |  GET     |  /orders            |             Return all of the Orders
| get_order    | GET    |  /orders/\<int:order_id>       |   Retrieve a single Order
| update_order | PUT     | /orders/\<int:order_id>      |   update an Order based the body that is posted
| delete_order   |   DELETE | /orders/\<int:order_id>   |    Delete an Order based on the id specified in the path

<!--
| update_order_items  | PUT | /orders/\<int:order_id>/items/\<int:item_id>  | Update an Order item based the body that is posted
| cancel_orders  | PUT  |  /orders/\<int:order_id>/cancel  |  Cancel all the items of the Order that have not been shipped yet
| cancel_item | PUT  | /orders/\<int:order_id>/items/\<int:item_id>/cancel | Cancel a single item in the Order that have not been shipped yet
| ship_orders  | PUT  |  /orders/\<int:order_id>/ship  |  Ship all the items in an Order
| ship_item | PUT |  /orders/\<int:order_id>/items/\<int:item_id>/ship | Ship a single item in the Order that have not been cancelled or delivered yet
| deliver_orders  | PUT  |  /orders/\<int:order_id>/deliver  |  Deliver all the items in an Order
| deliver_item | PUT |  /orders/\<int:order_id>/items/\<int:item_id>/deliver | Deliver a single item in the Order that has been shipped but not delivered or cancelled
-->
