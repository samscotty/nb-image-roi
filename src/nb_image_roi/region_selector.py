from IPython.display import display
from ipywidgets import Button, HBox, Layout, VBox
import numpy as np

from .ui.bbox import BBoxControls
from .ui.common import UIBase
from .ui.mpl import ImageRegionDisplay, ImageRegionSelect


class RegionSelector(UIBase, HBox):

    BBOX_STYLE = {"linewidth": 1, "edgecolor": "r", "facecolor": "none"}

    def __init__(self, image, minspan=5, hidden=False):
        """
        GUI for defining region of interest (ROI) on RGB image.

        Args:
            image: Array of image.
            minspan: Selections with xy-span less than minspan are ignored.
            hidden: Do not plot when initialised.

        """
        super().__init__()
        self.im = np.asarray(image)
        self._active = False

        # define widgets
        self.selector = self.add(ImageRegionSelect, image=self.im, minspan=minspan)
        self.sidebar = self.add(VBox, layout=Layout(margin="5px 0 0"))
        self.draw_button = Button(
            description="Draw",
            icon="drafting-compass",
            layout=Layout(width="105px"),
        )
        self.clear_button = Button(
            description="Clear",
            icon="trash-alt",
            disabled=True,
            layout=Layout(width="105px"),
        )
        self.buttons = self.add_to(
            self.sidebar,
            HBox,
            children=[self.draw_button, self.clear_button],
            layout=Layout(margin="0 0 30px 30px"),
        )
        self.controls = self.add_to(
            self.sidebar,
            BBoxControls,
            height=self.im.shape[0],
            width=self.im.shape[1],
            linewidth=self.BBOX_STYLE["linewidth"],
            minspan=minspan,
        )
        self.roi = self.add_to(self.sidebar, ImageRegionDisplay, image=self.get_roi())

        # event handlers
        self.controls.x.observe(self._update_region_handler, names="value")
        self.controls.y.observe(self._update_region_handler, names="value")
        self.controls.width.observe(self._update_region_handler, names="value")
        self.controls.height.observe(self._update_region_handler, names="value")
        self.draw_button.on_click(self._draw_region_handler)
        self.clear_button.on_click(self._clear_region_handler)

        # show on init
        if not hidden:
            display(self)

    def get_roi(self):
        """Array of selected region of interest.

        Note:
            Returns original image if no active region.

        Returns:
            Array of ROI.

        """
        return self.im[self.get_roi_slice()]

    def get_roi_slice(self):
        """Slice parameters of selected region of interest.

        Returns:
            Array slice of ROI.

        """
        if not self._active:
            return
        return self.controls.get_slice()

    def get_boundaries(self):
        """Boundaries of region of interest.

        Specifies x, y, width and height of selected box.

        Returns:
            ROI bounding box.

        """
        click = self.selector._click
        release = self.selector._release

        if not all(click) and not all(release):
            return

        xs, ys = zip(click, release)

        x = round(min(xs))
        y = round(min(ys))
        width = round(max(xs) - min(xs))
        height = round(max(ys) - min(ys))
        return {"x": x, "y": y, "width": width, "height": height}

    def get_inputs(self):
        """Inputs specified in bounding box controls.

        Returns:
            Bounding box inputs.

        """
        if not self._active:
            return
        return self.controls.get_inputs()

    def _draw_region_handler(self, _):
        bbox = self.get_boundaries()

        if not bbox:
            return

        self._active = True
        self.controls.set_inputs(**bbox)
        self.controls.show_inputs()
        self.selector.draw_roi(**bbox, **self.BBOX_STYLE)
        self.roi.plot(self.get_roi())
        self.draw_button.disabled = True
        self.clear_button.disabled = False

    def _clear_region_handler(self, _):
        self._active = False
        self.controls.hide_inputs()
        self.selector.remove_roi()
        self.roi.clear_plot()
        self.clear_button.disabled = True
        self.draw_button.disabled = False

    def _update_region_handler(self, _):
        self.selector.update_roi(**self.get_inputs())
        self.roi.clear_plot()
        self.roi.plot(image=self.get_roi())
