class Registry(dict):
    def __init__(self, *args, **kwargs):
        super(Registry, self).__init__(*args, **kwargs)
    
    @staticmethod
    def _register_generic(module_dict, cmd_clz, alias):
        assert alias not in module_dict
        module_dict[alias] = cmd_clz
    
    def register(self, alias_or_cmd_clz):
        if isinstance(alias_or_cmd_clz, str):
            alias = alias_or_cmd_clz
            
            def wrapper(cmd_clz):
                Registry._register_generic(self, cmd_clz, alias)
                return cmd_clz
            
            return wrapper
        
        else:
            cmd_clz = alias_or_cmd_clz
            alias = cmd_clz.__name__
            Registry._register_generic(self, cmd_clz, alias)
            return cmd_clz
