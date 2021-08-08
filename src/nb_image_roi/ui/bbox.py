from ipywidgets import BoundedIntText, VBox

from .common import UIBase


class BBoxControls(UIBase, VBox):
    def __init__(self, height, width, linewidth=1, minspan=2):
        """Input controls for box boundaries.

        Args:
            height: Height of image.
            width: Width of image.
            linewidth: Line width of box boundary.
            minspan: Minimum size of box.

        """
        super().__init__()

        self.x = self.add(BBoxInput, value=0, description="x", max=width - minspan)
        self.y = self.add(BBoxInput, value=0, description="y", max=height - minspan)
        self.width = self.add(BBoxInput, value=minspan, description="width", min=minspan, max=width)
        self.height = self.add(
            BBoxInput, value=minspan, description="height", min=minspan, max=height
        )
        self.linewidth = linewidth

    def get_slice(self):
        """Array slice of input boundaries.

        Note:
            ROI linewidth is used to offset slice.

        Returns:
            Box boundaries for array slicing.

        """
        return (
            slice(self.y.value + self.linewidth, self.y.value + self.height.value + self.linewidth),
            slice(self.x.value + self.linewidth, self.x.value + self.width.value + self.linewidth),
        )

    def set_inputs(self, x, y, width, height):
        """Set new input boundaries."""
        self.x.value = x
        self.y.value = y
        self.width.value = width
        self.height.value = height

    def show_inputs(self):
        """Set visibility of all inputs to 'visible'."""
        for child in self.children:
            child.show()

    def hide_inputs(self):
        """Set visibility of all inputs to 'hidden'."""
        for child in self.children:
            child.hide()


class BBoxInput(BoundedIntText):
    def __init__(self, **kwargs):
        """Input field for bounding box."""
        super().__init__(**kwargs)
        self.layout.width = "240px"
        self.layout.visibility = "hidden"

    def hide(self):
        self.layout.visibility = "hidden"

    def show(self):
        self.layout.visibility = "visible"
