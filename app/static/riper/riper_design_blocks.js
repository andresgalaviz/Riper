Blockly.Blocks['main'] = {
  init: function() {
    this.appendStatementInput("main_block")
        .setCheck(null)
        .appendField("main");
    this.setPreviousStatement(true, null);
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['if'] = {
  init: function() {
    this.appendValueInput("if_statement")
        .setCheck(null)
        .appendField("si");
    this.appendStatementInput("if_block")
        .setCheck(null)
        .appendField("entonces");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(225);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['function'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["string", "string"], ["bool", "bool"], ["void", "void"]]), "type")
        .appendField("funcion")
        .appendField(new Blockly.FieldTextInput("nombre"), "function_name");
    this.appendValueInput("function_parameters")
        .setCheck(null)
        .appendField("parametros");
    this.appendStatementInput("function_block")
        .setCheck(null)
        .appendField("Código");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(105);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['return'] = {
  init: function() {
    this.appendValueInput("return")
        .setCheck(null)
        .appendField("regresa");
    this.setPreviousStatement(true, null);
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['function_parameter'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["string", "string"], ["bool", "bool"]]), "type")
        .appendField(new Blockly.FieldTextInput("nombre"), "value_name");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['function_call'] = {
  init: function() {
    this.appendValueInput("parameters_in")
        .setCheck(null)
        .appendField("función")
        .appendField(new Blockly.FieldTextInput("nombre"), "function_name");
    this.setOutput(true, null);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['function_call_atomic'] = {
  init: function() {
    this.appendValueInput("parameters_in")
        .setCheck(null)
        .appendField("función")
        .appendField(new Blockly.FieldTextInput("nombre"), "function_name");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['parameters_input'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("parametros");
    this.appendStatementInput("parameters")
        .setCheck(null);
    this.setOutput(true, null);
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['else'] = {
  init: function() {
    this.appendStatementInput("else_block")
        .setCheck(null)
        .appendField("de otro modo");
    this.setPreviousStatement(true, ["if", "else_if"]);
    this.setNextStatement(true, null);
    this.setColour(225);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['else_if'] = {
  init: function() {
    this.appendValueInput("else_if_statement")
        .setCheck(null)
        .appendField("de otro modo si");
    this.appendStatementInput("if_block")
        .setCheck(null)
        .appendField("entonces");
    this.setPreviousStatement(true, "if");
    this.setNextStatement(true, null);
    this.setColour(225);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['expression'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Expresión");
    this.appendValueInput("left_operand")
        .setCheck("expression");
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["<", "<"], ["<=", "<="], [">", ">"], [">=", ">="], ["==", "=="], ["!=", "!="], ["&&", "&&"], ["||", "||"], ["+", "+"], ["-", "-"], ["*", "*"], ["/", "/"], ["%", "%"]]), "operator");
    this.appendValueInput("right_operand")
        .setCheck("expression");
    this.setOutput(true, null);
    this.setColour(290);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['var_declaration'] = {
  init: function() {
    this.appendValueInput("var_value")
        .setCheck(null)
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["string", "string"], ["bool", "bool"]]), "type")
        .appendField(new Blockly.FieldTextInput("nombre"), "var_name")
        .appendField("=");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['array_declaration'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("array")
        .appendField(new Blockly.FieldDropdown([["int", "int"], ["float", "float"], ["string", "string"], ["bool", "bool"]]), "type")
        .appendField(new Blockly.FieldTextInput("nombre"), "array_name")
        .appendField(new Blockly.FieldTextInput("[1][2]"), "array_dimensions");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(225);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['array_access'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("array")
        .appendField(new Blockly.FieldTextInput("nombre"), "array_name")
        .appendField(new Blockly.FieldTextInput("[0][0]"), "array_indexes");
    this.setOutput(true, null);
    this.setColour(160);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['var_access'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("variable")
        .appendField(new Blockly.FieldTextInput("nombre"), "var_name");
    this.setOutput(true, null);
    this.setColour(45);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['array_assign'] = {
  init: function() {
    this.appendValueInput("array_value")
        .setCheck(null)
        .appendField("array")
        .appendField(new Blockly.FieldTextInput("nombre"), "array_name")
        .appendField(new Blockly.FieldTextInput("[0][0]"), "array_indexes")
        .appendField("=");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(330);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['bool_constant'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["verdadero", "true"], ["falso", "false"]]), "bool_value");
    this.setOutput(true, null);
    this.setColour(260);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['int_constant'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldNumber(0), "int_constant");
    this.setOutput(true, null);
    this.setColour(20);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['float_constant'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldNumber(0), "int_part")
        .appendField(".")
        .appendField(new Blockly.FieldNumber(0), "decimal_part");
    this.setOutput(true, null);
    this.setColour(255);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['string_constant'] = {
  init: function() {
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput("'ejemplo'"), "string_constant");
    this.setOutput(true, null);
    this.setColour(0);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['for_loop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("for")
        .appendField(new Blockly.FieldTextInput("i = 0"), "for_expression")
        .appendField(new Blockly.FieldTextInput("i = i +1"), "for_increment");
    this.appendStatementInput("for_block")
        .setCheck(null);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(65);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['while_loop'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("while")
        .appendField(new Blockly.FieldTextInput("i < 10"), "while_expression");
    this.appendStatementInput("while_block")
        .setCheck(null);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['do_while'] = {
  init: function() {
    this.appendStatementInput("do_while_block")
        .setCheck(null)
        .appendField("do");
    this.appendDummyInput()
        .appendField("while")
        .appendField(new Blockly.FieldTextInput("i < 10"), "do_while_expression");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['console'] = {
  init: function() {
    this.appendValueInput("console_expression")
        .setCheck(null)
        .appendField("imprime");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(195);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['input'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("entrada")
        .appendField(new Blockly.FieldTextInput("'Dame un número'"), "input_message");
    this.setOutput(true, null);
    this.setColour(120);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['var_assign'] = {
  init: function() {
    this.appendValueInput("var_value")
        .setCheck(null)
        .appendField(new Blockly.FieldTextInput("variable"), "var_name")
        .appendField("=");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(290);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};

Blockly.Blocks['var_access_list'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("variable")
        .appendField(new Blockly.FieldTextInput("nombre"), "variable_name");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
    this.setTooltip('');
    this.setHelpUrl('http://www.example.com/');
  }
};