##############################################################################
# Copyright (c) 2016 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

"""to create heat templates from the base template
"""
import os
import json
import shutil
import common
import consts.parameters as parameters

class TreeNode:

    def __init__(self):
        self.up = None
        self.down = []
        self.variable_name = ''
        self.variable_value = 0

    def add_child(self, node):
        node.up = self
        self.down.append(node)

    def get_parent(self):
        return self.up

    def get_children(self):
        if len(self.down) == 0:
            return []
        return self.down

    def get_variable_name(self):
        return self.variable_name

    def get_variable_value(self):
        return self.variable_value

    def set_variable_name(self, name):
        self.variable_name = name

    def set_variable_value(self, value):
        self.variable_value = value

    def get_path(self):
        ret_val = []
        if not self.up:
            ret_val.append(self)
            return ret_val
        for node in self.up.get_path():
            ret_val.append(node)
        ret_val.append(self)
        return ret_val

    def __str__(self):
        return str(self.variable_name) + " --> " + str(self.variable_value)

    def __repr__(self):
        return str(self.variable_name) + " = " + str(self.variable_value)

    @staticmethod
    def _get_leaves(node, leaves):
        children = node.get_children()
        if len(children) == 0:
            leaves.append(node)
            return
        for child in children:
            TreeNode._get_leaves(child, leaves)

    @staticmethod
    def get_leaves(node):
        leaves = list()
        TreeNode._get_leaves(node, leaves)
        return leaves

template_name = parameters.TEST_TEMPLATE_NAME

def generates_templates(base_heat_template, deployment_configuration):
    # parameters loaded from file
    template_dir = common.get_template_dir()
    template_extension = parameters.TEMPLATE_EXTENSION
    template_base_name = base_heat_template

    variables = deployment_configuration

    # Delete the templates generated in previous running
    common.LOG.info("Removing the heat templates already generated")
    command = "rm {}{}_*".format(template_dir, template_name)
    os.system(command)

    # Creation of the tree with all the new configurations
    common.LOG.info("Creation of a tree with all new configurations")
    tree = TreeNode()
    for variable in variables:
        leaves = TreeNode.get_leaves(tree)
        common.LOG.debug("LEAVES: " + str(leaves))
        common.LOG.debug("VALUES: " + str(variables[variable]))

        for value in variables[variable]:
            for leaf in leaves:
                new_node = TreeNode()
                new_node.set_variable_name(variable)
                new_node.set_variable_value(value)
                leaf.add_child(new_node)

    common.LOG.debug("CONFIGURATION TREE: " + str(tree))

    common.LOG.info("Heat Template and metadata file creation")
    leaves = TreeNode.get_leaves(tree)
    counter = 1
    for leaf in leaves:
        heat_template_vars = leaf.get_path()
        if os.path.isabs(template_base_name):
            base_template = template_base_name
        else:
            base_template = template_dir + template_base_name
        new_template = template_dir + template_name
        new_template += "_" + str(counter) + template_extension
        shutil.copy(base_template, new_template)

        metadata = dict()
        for var in heat_template_vars:
            if var.get_variable_name():
                common.replace_in_file(new_template, "#" +
                                       var.get_variable_name(),
                                       var.get_variable_value())
                metadata[var.get_variable_name()] = var.get_variable_value()

        # Save the metadata on a JSON file
        with open(new_template + ".json", 'w') as outfile:
            json.dump(metadata, outfile)

        common.LOG.debug("Heat Templates and Metadata file " + str(counter) +
                         " created")
        counter += 1

    # Creation of the template files
    common.LOG.info(str(counter - 1) + " Heat Templates and Metadata files "
                                       "created")


def get_all_heat_templates(template_dir, template_extension):
    template_files = list()
    for dirname, dirnames, filenames in os.walk(template_dir):
        for filename in filenames:
            if template_extension in filename and filename.endswith(template_extension) and template_name in filename:
                template_files.append(filename)
    template_files.sort()
    return template_files
