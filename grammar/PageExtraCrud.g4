
parser grammar PageExtraCrud;

options { tokenVocab=ZmeiLangSimpleLexer; }

import Base;

an_crud:
    AN_CRUD
    an_crud_params
    ;

an_crud_params:
    BRACE_OPEN
    NL*
    an_crud_target_model
    an_crud_target_filter?
    (
         an_crud_theme
        |an_crud_skip
        |an_crud_fields
        |an_crud_list_fields
        |an_crud_pk_param
        |an_crud_item_name
        |an_crud_block
        |an_crud_object_expr
        |an_crud_can_edit
        |an_crud_url_prefix
        |NL
        |COMA
    )*
    NL*

    BRACE_CLOSE
    ;

// model

an_crud_target_model:
    (HASH id_or_kw) | classname;

// filter

an_crud_target_filter:
    code_block;

// theme

an_crud_theme:
    KW_THEME COLON id_or_kw;

// url_prefix

an_crud_url_prefix:
    KW_URL_PREFIX COLON an_crud_url_prefix_val;

an_crud_url_prefix_val:
    STRING_DQ | STRING_SQ;

// item_name

an_crud_item_name:
    KW_ITEM_NAME COLON id_or_kw;

// object_expr

an_crud_object_expr:
    KW_OBJECT_EXPR (code_line | COLON code_block);

// can_edit

an_crud_can_edit:
    KW_CAN_EDIT (code_line | COLON code_block);

// block

an_crud_block:
    KW_BLOCK COLON id_or_kw;

// pk_param

an_crud_pk_param:
    KW_PK_PARAM COLON id_or_kw;

// skip

an_crud_skip:
    KW_SKIP COLON an_crud_skip_values;

an_crud_skip_values:
    an_crud_view_name (COMA an_crud_view_name)*;

an_crud_view_name:
     KW_DELETE
    |KW_LIST
    |KW_CREATE
    |KW_EDIT
    |KW_DETAIL
    ;


// fields

an_crud_fields:
    KW_FIELDS COLON an_crud_fields_expr;

an_crud_fields_expr: an_crud_field (COMA an_crud_field)*;
an_crud_field: an_crud_field_spec an_crud_field_filter?;
an_crud_field_spec: STAR | (EXCLUDE? id_or_kw);
an_crud_field_filter: code_block;

// list fields

an_crud_list_fields:
    KW_LIST_FIELDS COLON an_crud_list_fields_expr;

an_crud_list_fields_expr: an_crud_list_field (COMA an_crud_list_field)*;
an_crud_list_field: an_crud_list_field_spec;
an_crud_list_field_spec: STAR | (EXCLUDE? id_or_kw);