from ipywidgets import VBox
from matplotlib import patches
from matplotlib import pyplot as plt
from matplotlib.widgets import RectangleSelector

from .common import UIBase


class ImageBase(UIBase, VBox):
    def __init__(self, image, hidden=False, **kwargs):
        """Base class for matplotlib image widget.

        Args:
            image: Array of image.
            hidden: Do not plot when initialised.

        """
        super().__init__()

        kwargs.setdefault("constrained_layout", True)
        plt.ioff()
        self.fig, self.ax = plt.subplots(**kwargs)
        plt.ion()

        self.canvas = self._add_instance(self.fig.canvas)
        self.canvas.header_visible = False
        self.canvas.footer_visible = False
        self.canvas.resizable = False

        self.ax.axis("off")

        if not hidden:
            self.plot(image)

    def plot(self, image):
        self.ax.imshow(image, vmin=0, vmax=255)

    def clear_plot(self):
        self.ax.clear()
        self.ax.axis("off")


class ImageRegionSelect(ImageBase):
    def __init__(self, image, figsize=(7, 5), minspan=5):
        """Interactive figure for selecting region of interest on an image.

        Args:
            image: Array of image.
            figsize (optional): Width, height of matplotlib figure (in inches).
            minspan (optional): Selections with xy-span less than minspan are ignored.

        """
        super().__init__(image, figsize=figsize)

        self.rs = RectangleSelector(
            self.ax,
            self._select_callback,
            drawtype="box",
            useblit=False,
            rectprops=dict(edgecolor="red", linewidth=1.2, fill=False),
            minspanx=minspan,
            minspany=minspan,
            spancoords="pixels",
            interactive=True,
        )

        self.canvas.toolbar_position = "bottom"
        self.canvas.mpl_connect("key_press_event", self._toggle_selector)

        self._click = [None, None]
        self._release = [None, None]

    def draw_roi(self, x, y, width, height, **kwargs):
        """Add region of interest to figure."""
        roi = ROI(x=x, y=y, width=width, height=height)
        self.ax.add_patch(roi.draw(**kwargs))
        self.rs.set_visible(False)

    def remove_roi(self):
        """Remove region of interest from figure."""
        self.ax.patches[-1].remove()
        self.rs.set_visible(True)

    def update_roi(self, x, y, width, height):
        """Update region of interest on figure."""
        self._click[:] = [x, y]
        self._release[:] = [x + width, y + height]
        self.rs.extents = (x, x + width, y, y + height)
        self.ax.patches[-1].set_bounds(x, y, width, height)

    def _select_callback(self, eclick, erelease):
        self._click[:] = eclick.xdata, eclick.ydata
        self._release[:] = erelease.xdata, erelease.ydata

    def _toggle_selector(self, event):
        if event.key == "t":
            if self.rs.active:
                self.rs.set_active(False)
            else:
                self.rs.set_active(True)


class ImageRegionDisplay(ImageBase):
    def __init__(self, image, figsize=(3, 3)):
        """Interactive figure for displaying the region of interest.

        Args:
            image: Array of image.
            figsize (optional): Width, height of matplotlib figure (in inches).

        """
        super().__init__(image, hidden=True, figsize=figsize)
        self.canvas.toolbar_visible = False


class ROI:
    def __init__(self, x=0, y=0, width=100, height=100):
        """Region of Interest (ROI)."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, patch="Rectangle", **kwargs):
        """Create matplotlib patch for ROI."""
        return getattr(patches, patch)(
            xy=(self.x, self.y),
            width=self.width,
            height=self.height,
            **kwargs,
        )
