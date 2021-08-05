class UIBase:
    """
    Base class for UI containers.
    Provides some convenience functions to add and remove components.
    """

    def add_to(self, container, component, **kwargs):
        """Create component with kwargs and add it to the container's
        children, return the created component.
        """
        component_instance = component(**kwargs)
        return self._add_instance_to(container, component_instance)

    def add(self, component, **kwargs):
        """Create component with kwargs and add it to self, return the created component."""
        return self.add_to(self, component, **kwargs)

    def remove_from(self, container, component):
        """Remove the component from the container."""
        children = list(container.children)
        try:
            children.remove(component)
        except ValueError:
            pass
        container.children = children

    def _add_instance_to(self, container, component_instance):
        """Add component_instance to the container's children, return the component."""
        container.children += (component_instance,)
        return component_instance

    def _add_instance(self, component_instance):
        """Add component_instance to self, return the component."""
        return self._add_instance_to(self, component_instance)

    def _remove(self, component):
        """Remove the component from self."""
        self.remove_from(self, component)
