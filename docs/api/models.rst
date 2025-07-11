Models API Reference
===================

This page provides detailed API documentation for the microlensing models in GCMicrolensing.

Single Lens Models
-----------------

.. automodule:: GCMicrolensing.models
   :members:
   :undoc-members:
   :show-inheritance:

OneL1S
~~~~~~

.. autoclass:: GCMicrolensing.models.OneL1S
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   .. automethod:: __init__

Binary Lens Models
-----------------

TwoLens1S
~~~~~~~~~

.. autoclass:: GCMicrolensing.models.TwoLens1S
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   .. automethod:: __init__

Triple Lens Models
-----------------

ThreeLens1SVBM
~~~~~~~~~~~~~~

.. autoclass:: GCMicrolensing.models.ThreeLens1SVBM
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   .. automethod:: __init__

ThreeLens1S
~~~~~~~~~~~

.. autoclass:: GCMicrolensing.models.ThreeLens1S
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   .. automethod:: __init__

Model Parameters
---------------

Common Parameters
~~~~~~~~~~~~~~~~~

All microlensing models share these common parameters:

* **t0** (float): Time of closest approach in days
* **tE** (float): Einstein crossing time in days  
* **rho** (float): Source radius in units of Einstein radius
* **u0_list** (array-like): List of impact parameters

Binary Lens Parameters
~~~~~~~~~~~~~~~~~~~~~~

* **q** (float): Mass ratio of the second lens to the first lens
* **s** (float): Separation between the two lenses in units of Einstein radius
* **alpha** (float): Source trajectory angle in degrees

Triple Lens Parameters
~~~~~~~~~~~~~~~~~~~~~~

* **q2** (float): Mass ratio of the second lens to the first lens
* **q3** (float): Mass ratio of the third lens to the first lens
* **s12** (float): Separation between first and second lenses
* **s23** (float): Separation between second and third lenses (VBM)
* **s2** (float): Separation between first and second lenses (TripleLensing)
* **s3** (float): Separation between first and third lenses (TripleLensing)
* **alpha** (float): Source trajectory angle in degrees
* **psi** (float): Angle between lens triangle and source trajectory (VBM)
* **psi_deg** (float): Angle between second and third lenses (TripleLensing)

TripleLensing-Specific Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **rs** (float): Source radius for image calculations
* **secnum** (int): Number of sectors for image finding
* **basenum** (int): Base number for image finding algorithm
* **num_points** (int): Number of time points for calculations

Model Methods
-------------

All models provide these common methods:

* **plot_light_curve()**: Plot light curves for all impact parameters
* **animate()**: Create an animation of the microlensing event
* **show_all()**: Create a comprehensive view with all plots

Additional methods vary by model:

OneL1S Methods
~~~~~~~~~~~~~~

* **plot_centroid_shift()**: Plot astrometric centroid shifts
* **plot_light_curve_on_ax(ax)**: Plot on provided matplotlib axis
* **plot_centroid_shift_on_ax(ax)**: Plot centroid shift on provided axis

TwoLens1S Methods
~~~~~~~~~~~~~~~~~

* **plot_caustic_critical_curves()**: Plot caustic and critical curves
* **plot_centroid_trajectory()**: Plot centroid shift trajectories
* **plot_centroid_shift()**: Plot centroid shift magnitude vs time

ThreeLens1SVBM Methods
~~~~~~~~~~~~~~~~~~~~~~

* **plot_caustic_critical_curves()**: Plot caustic and critical curves
* **plot_different_q3_lc()**: Plot light curves for different q3 values

ThreeLens1S Methods
~~~~~~~~~~~~~~~~~~~

* **plot_caustics_and_critical()**: Plot caustics using VBMicrolensing
* **plot_centroid_trajectory()**: Plot centroid shift trajectories
* **plot_shift_vs_time()**: Plot centroid shift magnitude vs time
* **animate_combined()**: Combined animation with both backends
* **get_lens_geometry()**: Get lens geometry parameters

Mathematical Background
----------------------

The models implement the gravitational lens equation:

.. math::

   \vec{\beta} = \vec{\theta} - \vec{\alpha}(\vec{\theta})

where:
* :math:`\vec{\beta}` is the source position
* :math:`\vec{\theta}` is the image position  
* :math:`\vec{\alpha}` is the deflection angle

For multiple lenses, the deflection angle is the sum of individual lens contributions:

.. math::

   \vec{\alpha}(\vec{\theta}) = \sum_i \frac{m_i (\vec{\theta} - \vec{\theta}_i)}{|\vec{\theta} - \vec{\theta}_i|^2}

where :math:`m_i` and :math:`\vec{\theta}_i` are the mass and position of the i-th lens. 