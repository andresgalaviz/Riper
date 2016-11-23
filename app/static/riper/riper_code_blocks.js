Blockly.JavaScript['main'] = function(block) {
  var statements_main_block = Blockly.JavaScript.statementToCode(block, 'main_block');
  // TODO: Assemble JavaScript into code variable.
  var code = 'main(){ ' + statements_main_block + '} ';
  return code;
};

Blockly.JavaScript['if'] = function(block) {
  var value_if_statement = Blockly.JavaScript.valueToCode(block, 'if_statement', Blockly.JavaScript.ORDER_ATOMIC);;
  var statements_if_block = Blockly.JavaScript.statementToCode(block, 'if_block');
  // TODO: Assemble JavaScript into code variable.
  var code = 'if(' + value_if_statement + ')  {   '+ statements_if_block + ' } ';
  return code;
};

Blockly.JavaScript['function'] = function(block) {
  var dropdown_type = block.getFieldValue('type');
  var text_function_name = block.getFieldValue('function_name');
  var value_function_parameters = Blockly.JavaScript.valueToCode(block, 'function_parameters', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_function_block = Blockly.JavaScript.statementToCode(block, 'function_block');
  
  // TODO: Assemble JavaScript into code variable.
  var code = 'function ' + dropdown_type + ' ' + text_function_name + '(' + value_function_parameters + ')  {  ' + statements_function_block + ' } ';
  
  return code;
};

Blockly.JavaScript['return'] = function(block) {
  var value_return = Blockly.JavaScript.valueToCode(block, 'return', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = 'return ' + value_return + '; ';
  return code;
};

Blockly.JavaScript['function_parameter'] = function(block) {
  var dropdown_type = block.getFieldValue('type');
  var text_value_name = block.getFieldValue('value_name');
  // TODO: Assemble JavaScript into code variable.
  var code = dropdown_type + ' ' + text_value_name + ',';
  return code;
};

Blockly.JavaScript['function_call'] = function(block) {
  var text_function_name = block.getFieldValue('function_name');
  var value_parameters_in = Blockly.JavaScript.valueToCode(block, 'parameters_in', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = text_function_name + '(' + value_parameters_in + ')';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['function_call_atomic'] = function(block) {
  var text_function_name = block.getFieldValue('function_name');
  var value_parameters_in = Blockly.JavaScript.valueToCode(block, 'parameters_in', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = text_function_name + '(' + value_parameters_in + '); ';
  return code;
};

Blockly.JavaScript['parameters_input'] = function(block) {
  var statements_parameters = Blockly.JavaScript.statementToCode(block, 'parameters').slice(0, -1);
  
  // TODO: Assemble JavaScript into code variable.
  var code = statements_parameters;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_ATOMIC];
};

Blockly.JavaScript['else'] = function(block) {
  var statements_else_block = Blockly.JavaScript.statementToCode(block, 'else_block');
  // TODO: Assemble JavaScript into code variable.
  var code = 'else {  ' + statements_else_block + ' } ';
  return code;
};

Blockly.JavaScript['else_if'] = function(block) {
  var value_else_if_statement = Blockly.JavaScript.valueToCode(block, 'else_if_statement', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_if_block = Blockly.JavaScript.statementToCode(block, 'if_block');
  // TODO: Assemble JavaScript into code variable.
  var code = 'elif(' +value_else_if_statement + ')' + ' {  ' + statements_if_block + ' } ';
  return code;
};

Blockly.JavaScript['expression'] = function(block) {
  var value_left_operand = Blockly.JavaScript.valueToCode(block, 'left_operand', Blockly.JavaScript.ORDER_ATOMIC);
  var dropdown_operator = block.getFieldValue('operator');
  var value_right_operand = Blockly.JavaScript.valueToCode(block, 'right_operand', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = value_left_operand + ' ' + dropdown_operator + ' ' + value_right_operand;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['var_declaration'] = function(block) {
  var dropdown_type = block.getFieldValue('type');
  var text_var_name = block.getFieldValue('var_name');
  var value_var_value = Blockly.JavaScript.valueToCode(block, 'var_value', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = dropdown_type + ' ' + text_var_name + ' = ' + value_var_value + '; ';
  return code;
};

Blockly.JavaScript['array_declaration'] = function(block) {
  var dropdown_type = block.getFieldValue('type');
  var text_array_name = block.getFieldValue('array_name');
  var text_array_dimensions = block.getFieldValue('array_dimensions');
  // TODO: Assemble JavaScript into code variable.
  var code = 'array ' + dropdown_type + ' ' + text_array_name + text_array_dimensions + '; ';
  return code;
};

Blockly.JavaScript['array_access'] = function(block) {
  var text_array_name = block.getFieldValue('array_name');
  var text_array_indexes = block.getFieldValue('array_indexes');
  // TODO: Assemble JavaScript into code variable.
  var code = text_array_name + text_array_indexes;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['var_access'] = function(block) {
  var text_var_name = block.getFieldValue('var_name');
  // TODO: Assemble JavaScript into code variable.
  var code = text_var_name;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['var_access_list'] = function(block) {
  var text_variable_name = block.getFieldValue('variable_name');
  // TODO: Assemble JavaScript into code variable.
  var code = text_variable_name + ',';
  return code;
};

Blockly.JavaScript['array_assign'] = function(block) {
  var text_array_name = block.getFieldValue('array_name');
  var text_array_indexes = block.getFieldValue('array_indexes');
  var value_array_value = Blockly.JavaScript.valueToCode(block, 'array_value', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  
  var code = text_array_name + text_array_indexes + ' = ' + value_array_value + ';';
  return code;
};

Blockly.JavaScript['bool_constant'] = function(block) {
  var dropdown_bool_value = block.getFieldValue('bool_value');
  // TODO: Assemble JavaScript into code variable.
  var code = dropdown_bool_value;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['int_constant'] = function(block) {
  var number_int_constant = block.getFieldValue('int_constant');
  // TODO: Assemble JavaScript into code variable.
  var code = number_int_constant;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['float_constant'] = function(block) {
  var number_int_part = block.getFieldValue('int_part');
  var number_decimal_part = block.getFieldValue('decimal_part');
  // TODO: Assemble JavaScript into code variable.
  var code = number_int_part + '.' + number_decimal_part;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['string_constant'] = function(block) {
  var text_string_constant = block.getFieldValue('string_constant');
  // TODO: Assemble JavaScript into code variable.
  var code = '\'' + text_string_constant + '\'';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['for_loop'] = function(block) {
  var text_for_expression = block.getFieldValue('for_expression');
  var text_for_increment = block.getFieldValue('for_increment');
  var statements_for_block = Blockly.JavaScript.statementToCode(block, 'for_block');
  // TODO: Assemble JavaScript into code variable.
  var code = 'for(' + text_for_expression + ';' + text_for_increment + ';)  {  ' + statements_for_block + '}';
  return code;
};

Blockly.JavaScript['while_loop'] = function(block) {
  var text_while_expression = block.getFieldValue('while_expression');
  var statements_while_block = Blockly.JavaScript.statementToCode(block, 'while_block');
  // TODO: Assemble JavaScript into code variable.
  var code = 'while(' + text_while_expression + ')  {  ' + statements_while_block + '}';
  return code;
};

Blockly.JavaScript['do_while'] = function(block) {
  var statements_do_while_block = Blockly.JavaScript.statementToCode(block, 'do_while_block');
  var text_do_while_expression = block.getFieldValue('do_while_expression');
  // TODO: Assemble JavaScript into code variable.
  var code = 'do { ' + statements_do_while_block + ' } while(' +  text_do_while_expression + ');';
  return code;
};

Blockly.JavaScript['console'] = function(block) {
  var value_console_expression = Blockly.JavaScript.valueToCode(block, 'console_expression', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = 'console(' + value_console_expression + ');  ';
  return code;
};

Blockly.JavaScript['input'] = function(block) {
  var text_input_message = block.getFieldValue('input_message');
  // TODO: Assemble JavaScript into code variable.
  var code = 'input(' + text_input_message + ');  ';
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};

Blockly.JavaScript['var_assign'] = function(block) {
  var text_var_name = block.getFieldValue('var_name');
  var value_var_value = Blockly.JavaScript.valueToCode(block, 'var_value', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = text_var_name + ' = ' + value_var_value + ';';
  return code;
};