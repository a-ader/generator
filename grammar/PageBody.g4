parser grammar PageBase;

options { tokenVocab=ZmeiLangSimpleLexer; }

import Base,
       PageExtra
       ;

/**************************
 * Pages
 **************************/

page_body:
    page_field*

    page_function*

    page_code?

    NL*
    page_annotation*
    ;

page_code: python_code;

page_field:
    page_field_name
    ASSIGN
    page_field_code
    (NL+|EOF)
    ;

page_field_name : id_or_kw ;

page_field_code : PYTHON_CODE;


page_function:
    page_function_name
    BRACE_OPEN
    page_function_args?
    BRACE_CLOSE
    code_block?
    (NL+|EOF)
    ;

page_function_name : id_or_kw ;

page_function_args : id_or_kw (COMA id_or_kw)*;
