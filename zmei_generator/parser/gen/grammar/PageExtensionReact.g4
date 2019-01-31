
parser grammar PageExtensionReact;

options { tokenVocab=ZmeiLangSimpleLexer; }

import Base;

an_react:
    (an_react_type)
    (DOT an_react_descriptor)?
    ;

an_react_type : AN_REACT|AN_REACT_CLIENT|AN_REACT_SERVER ;

an_react_descriptor: id_or_kw;