# This code was orignally written for the Glumpy project and is being
# used here with slight modifications.
#
# Copyright notice from the original source:
#
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
#
# The full license text for Glumpy has been included in
# LICENSES/glumpy.txt

class GLObject:
    """Generic GL object that may live both on CPU and GPU"""

    # Internal id counter to keep track of GPU objects
    _idcount = 0

    def __init__(self):
        """Initialize the object in the default state"""
        self._handle = -1
        self._target = None
        self._need_setup = True
        self._need_create = True
        self._need_update = True
        self._need_delete = False

        GLObject._idcount += 1
        self._id = GLObject._idcount

    @property
    def need_create(self):
        """Whether object needs to be created"""
        return self._need_create


    @property
    def need_update(self):
        """Whether object needs to be updated """
        return self._need_update

    @property
    def need_setup(self):
        """Whether object needs to be setup"""
        return self._need_setup

    @property
    def need_delete(self):
        """Whether object needs to be deleted"""
        return self._need_delete


    def delete(self):
        """Delete the object from GPU memory"""
        #if self.need_delete:
        self._delete()
        self._handle = -1
        self._need_setup = True
        self._need_create = True
        self._need_update = True
        self._need_delete = False


    def activate(self):
        """Activate the object on GPU"""

        if hasattr(self, 'base') and isinstance(self.base, GLObject):
            self.base.activate()
            return

        if self.need_create:
            self._create()
            self._need_create = False

        self._activate()

        if self.need_setup:
            self._setup()
            self._need_setup = False

        if self.need_update:
            self._update()
            self._need_update = False


    def deactivate(self):
        """Deactivate the object on GPU."""

        if hasattr(self,"base") and isinstance(self.base,GLObject):
            self.base.deactivate()
        else:
            self._deactivate()

    @property
    def handle(self):
        """Name of this object on the GPU"""
        if hasattr(self, "base") and isinstance(self.base, GLObject):
            if hasattr(self.base, "_handle"):
                return self.base._handle
        return self._handle

    @property
    def target(self):
        """OpenGL type of object."""
        if hasattr(self, "base") and isinstance(self.base,GLObject):
            return self.base._target
        return self._target

    def _activate(self):
        pass

    def _deactivate(self):
        pass

    def _delete(self):
        pass

    def _create(self):
        pass

    def _setup(self):
        pass

    def _update(self):
        pass

    def __repr__(self):
        return "GLObject( id={} )".format(self._id)

    __str__ = __repr__
