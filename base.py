class Base:
    def __init_subclass__(cls, *a, **kw):
        """Enforces all abstract methods are overriden in derived  classes

        Raises:
            NotImplementedError
        """
        super().__init_subclass__(*a, **kw)
        for attr in dir(cls):
            method = getattr(cls, attr)
            if getattr(method, '__isabstractmethod__', False) and not attr in cls.__dict__:
                raise NotImplementedError(f"Method '{attr}' must be overriden!")