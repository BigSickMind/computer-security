def is_keyword(word):
    keywords = ['alignas', 'alignof', 'and', 'and_eq', 'asm', 'atomic_cancel', 'atomic_commit', 'atomic_noexcept',
                'auto', 'bitand', 'bitor', 'bool', 'break', 'case', 'catch', 'char', 'char16_t', 'char32_t', 'class',
                'compl', 'concept', 'const', 'constexpr', 'const_cast', 'continue', 'co_await', 'co_return', 'co_yield',
                'decltype', 'default', 'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum', 'explicit', 'extern',
                'false', 'float', 'for', 'friend', 'goto', 'if', 'inline', 'int', 'long', 'module', 'mutable',
                'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr', 'operator', 'or', 'or_eq', 'private',
                'protected', 'public', 'register', 'reinterpret_cast', 'requires', 'return', 'short', 'signed',
                'sizeof', 'static', 'static_assert', 'static_cast', 'struct', 'switch', 'synchronized', 'template',
                'this', 'thread_local', 'throw', 'true', 'try', 'typedef', 'typeid', 'typename', 'union', 'unsigned',
                'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq', 'main', 'false', 'true',
                'vector', 'map', 'set', 'std', 'endl', 'cin', 'cout', 'INT_MAX', 'make_pair', 'for', 'while', 'include',
                'sync_with_stdio', 'scanf', 'printf', 'push_back', 'size', 'first', 'second', 'begin', 'end', 'pair',
                'sort']
    if word in keywords:
        return True
    return False
