# coding=utf-8
from __future__ import absolute_import

__author__ = "Gina Häußge <osd@foosel.net>"
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'
__copyright__ = "Copyright (C) 2014 The OctoPrint Project - Released under terms of the AGPLv3 License"


from .core import Plugin


class StartupPlugin(Plugin):
	"""
	The ``StartupPlugin`` allows hooking into the startup of OctoPrint. It can be used to start up additional services
	on or just after the startup of the server.
	"""

	def on_startup(self, host, port):
		"""
		Called just before the server is actually launched. Plugins get supplied with the ``host`` and ``port`` the server
		will listen on. Note that the ``host`` may be ``0.0.0.0`` if it will listen on all interfaces, so you can't just
		blindly use this for constructing publicly reachable URLs. Also note that when this method is called, the server
		is not actually up yet and none of your plugin's APIs or blueprints will be reachable yet. If you need to be
		externally reachable, use :func:`on_after_startup` instead or additionally.

		:param string host: the host the server will listen on, may be ``0.0.0.0``
		:param int port:    the port the server will listen on
		"""

		pass

	def on_after_startup(self):
		"""
		Called just after launch of the server, so when the listen loop is actually running already.
		"""

		pass


class ShutdownPlugin(Plugin):
	"""
	The ``ShutdownPlugin`` allows hooking into the shutdown of OctoPrint. It's usually used in conjunction with the
	:class:`StartupPlugin` mixin, to cleanly shut down additional services again that where started by the :class:`StartupPlugin`
	part of the plugin.
	"""

	def on_shutdown(self):
		"""
		Called upon the imminent shutdown of OctoPrint.
		"""
		pass


class AssetPlugin(Plugin):
	"""
	The ``AssetPlugin`` mixin allows plugins to define additional static assets such as Javascript or CSS files to
	be automatically embedded into the pages delivered by the server to be used within the client sided part of
	the plugin.

	A typical usage of the ``AssetPlugin`` functionality is to embed a custom view model to be used by templates injected
	through :class:`TemplatePlugin`s.
	"""

	def get_asset_folder(self):
		"""
		Defines the folder where the plugin stores its static assets as defined in :func:`get_assets`. Override this if
		your plugin stores its assets at some other place than the ``static`` sub folder in the plugin base directory.

		:return string: the absolute path to the folder where the plugin stores its static assets
		"""
		import os
		return os.path.join(self._basefolder, "static")

	def get_assets(self):
		"""
		Defines the static assets the plugin offers. The following asset types are recognized and automatically
		imported at the appropriate places to be available:

		js
		   Javascript files, such as additional view models
		css
		   CSS files with additional styles, will be embedded into delivered pages when not running in LESS mode.
		less
		   LESS files with additional styles, will be embedded into delivered pages when running in LESS mode.

		The expected format to be returned is a dictionary mapping one or more of these keys to a list of files of that
		type, the files being represented as relative paths from the asset folder as defined via :func:`get_asset_folder`.
		Example:

		.. code-block:: python

		   def get_assets(self):
		       return dict(
		           js=['js/my_file.js', 'js/my_other_file.js'],
		           css=['css/my_styles.css'],
		           less=['less/my_styles.less']
		        )

		The assets will be made available by OctoPrint under the URL ``/plugin_assets/<plugin identifier>/<path>``, with
		``plugin identifier`` being the plugin's identifier and ``path`` being the path as defined in the asset dictionary.

		:return dict: a dictionary describing the static assets to publish for the plugin
		"""
		return dict()


class TemplatePlugin(Plugin):
	"""
	Using the ``TemplatePlugin`` mixin plugins may inject their own components into the OctoPrint web interface.

	Currently OctoPrint supports the following types of injections:

	Navbar
	   The right part of the navigation bar located at the top of the UI can be enriched with additional links. Note that
	   with the current implementation, plugins will always be located *to the left* of the existing links.

	   The included template must be called ``<pluginname>_navbar.jinja2`` (e.g. ``myplugin_navbar.jinja2``) unless
	   overridden by the configuration supplied through :func:`get_template_configs`.

	   The template will be already wrapped into the necessary structure, plugins just need to supply the pure content. The
	   wrapper structure will have all additional classes and styles applied as specified via the configuration supplied
	   through :func:`get_template_configs`.

	Sidebar
	   The left side bar containing Connection, State and Files sections can be enriched with additional sections. Note
	   that with the current implementations, plugins will always be located *beneath* the existing sections.

	   The included template must be called ``<pluginname>_sidebar.jinja2`` (e.g. ``myplugin_sidebar.jinja2``) unless
	   overridden by the configuration supplied through :func:`get_template_configs`.

	   The template will be already wrapped into the necessary structure, plugins just need to supply the pure content. The
	   wrapper divs for both the whole box as well as the content pane will have all additional classes and styles applied
	   as specified via the configuration supplied through :func:`get_template_configs`.

	Tabs
	   The available tabs of the main part of the interface may be extended with additional tabs originating from within
	   plugins. Note that with the current implementation, plugins will always be located *to the right* of the existing
	   tabs.

	   The included template must be called ``<pluginname>_tab.jinja2`` (e.g. ``myplugin_tab.jinja2``) unless
	   overridden by the configuration supplied through :func:`get_template_configs`.

	   The template will be already wrapped into the necessary structure, plugins just need to supply the pure content. The
	   wrapper div and the link in the navigation will have the additional classes and styles applied as specified via the
	   configuration supplied through :func:`get_template_configs`.

	Settings
	   Plugins may inject a dialog into the existing settings view. Note that with the current implementations, plugins
	   will always be listed beneath the "Plugins" header in the settings link list, ordered alphabetically after
	   their displayed name.

	   The included template must be called ``<pluginname>_settings.jinja2`` (e.g. ``myplugin_settings.jinja2``) unless
	   overridden by the configuration supplied through :func:`get_template_configs`.

	   The template will be already wrapped into the necessary structure, plugins just need to supply the pure content. The
	   wrapper div and the link in the navigation will have the additional classes and styles applied as defined via the
	   supplied configuration supplied through :func:`get_template_configs`.

	Generic
	   Plugins may also inject arbitrary templates into the page of the web interface itself, e.g. in order to
	   add overlays or dialogs to be called from within the plugin's javascript code.

	.. figure:: ../images/template-plugin-types-main.png
	   :align: center
	   :alt: Template injection types in the main part of the interface

	   Template injection types in the main part of the interface

	.. figure:: ../images/template-plugin-types-settings.png
	   :align: center
	   :alt: Template injection types in the settings

	   Template injection types in the settings

	You can find an example for a simple plugin which injects navbar, sidebar, tab and settings content into the interface in
	`the "helloworld" plugin in OctoPrint's collection of plugin examples <https://github.com/OctoPrint/Plugin-Examples/tree/master/helloworld>`_.
	"""

	def get_template_configs(self):
		"""
		Allows configuration of injected navbar, sidebar, tab and settings templates. Should be a list containing one
		configuration object per template to inject. Each configuration object is represented by a dictionary with a mandatory key
		``type`` encoding the template type the configuration is targeting. Possible values here are ``navbar``, ``sidebar``,
		``tab``, ``settings`` and ``generic``.

		Further keys to be included in the dictionary depend on the type:

		``navbar`` type
		   .. figure:: ../images/template-plugin-type-navbar.png
		      :align: center
		      :alt: Structure of navbar plugins

		   Configures a navbar component to inject. The following keys are supported:

		   .. list-table::
		      :widths: 5 95

		      * - template
		        - Name of the template to inject, defaults to ``<pluginname>_navbar.jinja2``.
		      * - suffix
		        - Suffix to attach to the element ID of the injected template, will be ``_<index>`` if not provided and not
		          the first template of the type, with ``index`` counting from 1 and increasing for each template of the same
		          type.
		      * - custom_bindings
		        - A boolean value indicating whether the default view model should be bound to the navbar entry (``false``)
		          or if a custom binding will be used by the plugin (``true``, default).
		      * - data_bind
		        - Additional knockout data bindings to apply to the navbar entry, can be used to add further behaviour to
		          the container based on internal state if necessary.
		      * - classes
		        - Additional classes to apply to the navbar entry, as a list of individual classes
		          (e.g. ``classes=["myclass", "myotherclass"]``) which will be joined into the correct format by the template engine.
		      * - styles
		        - Additional CSS styles to apply to the navbar entry, as a list of individual declarations
		          (e.g. ``styles=["color: red", "display: block"]``) which will be joined into the correct format by the template
		          engine.

		``sidebar`` type
		   .. figure:: ../images/template-plugin-type-sidebar.png
		      :align: center
		      :alt: Structure of sidebar plugins

		   Configures a sidebar component to inject. The following keys are supported:

		   .. list-table::
		      :widths: 5 95

		      * - name
		        - The name of the sidebar entry, if not set the name of the plugin will be used.
		      * - icon
		        - Icon to use for the sidebar header, should be the name of a Font Awesome icon without the leading ``icon-`` part.
		      * - template
		        - Name of the template to inject, defaults to ``<pluginname>_sidebar.jinja2``.
		      * - template_header
		        - Additional template to include in the head section of the sidebar item. For an example of this, see the additional
		          options included in the "Files" section.
		      * - suffix
		        - Suffix to attach to the element ID of the injected template, will be ``_<index>`` if not provided and not
		          the first template of the type, with ``index`` counting from 1 and increasing for each template of the same
		          type.
		      * - custom_bindings
		        - A boolean value indicating whether the default view model should be bound to the sidebar container (``false``)
		          or if a custom binding will be used by the plugin (``true``, default).
		      * - data_bind
		        - Additional knockout data bindings to apply to the template container, can be used to add further behaviour to
		          the container based on internal state if necessary.
		      * - classes
		        - Additional classes to apply to both the wrapper around the sidebar box as well as the content pane itself, as a
		          list of individual classes (e.g. ``classes=["myclass", "myotherclass"]``) which will be joined into the correct
		          format by the template engine.
		      * - classes_wrapper
		        - Like ``classes`` but only applied to the whole wrapper around the sidebar box.
		      * - classes_content
		        - Like ``classes`` but only applied to the content pane itself.
		      * - styles
		        - Additional CSS styles to apply to both the wrapper around the sidebar box as well as the content pane itself,
		          as a list of individual declarations (e.g. ``styles=["color: red", "display: block"]``) which will be joined
		          into the correct format by the template engine.
		      * - styles_wrapper
		        - Like ``styles`` but only applied to the whole wrapper around the sidebar box.
		      * - styles_content
		        - Like ``styles`` but only applied to the content pane itself

		``tab`` type
		   .. figure:: ../images/template-plugin-type-tab.png
		      :align: center
		      :alt: Structure of tab plugins

		   Configures a tab component to inject. The value must be a dictionary, supported values are the following:

		   .. list-table::
		      :widths: 5 95

		      * - name
		        - The name under which to include the tab, if not set the name of the plugin will be used.
		      * - template
		        - Name of the template to inject, defaults to ``<pluginname>_tab.jinja2``.
		      * - suffix
		        - Suffix to attach to the element ID of the injected template, will be ``_<index>`` if not provided and not
		          the first template of the type, with ``index`` counting from 1 and increasing for each template of the same
		          type.
		      * - custom_bindings
		        - A boolean value indicating whether the default view model should be bound to the tab pane and link
		          in the navigation (``false``) or if a custom binding will be used by the plugin (``true``, default).
		      * - data_bind
		        - Additional knockout data bindings to apply to the template container, can be used to add further behaviour to
		          the container based on internal state if necessary.
		      * - classes
		        - Additional classes to apply to both the wrapper around the sidebar box as well as the content pane itself, as a
		          list of individual classes (e.g. ``classes=["myclass", "myotherclass"]``) which will be joined into the correct
		          format by the template engine.
		      * - classes_link
		        - Like ``classes`` but only applied to the link in the navigation.
		      * - classes_content
		        - Like ``classes`` but only applied to the content pane itself.
		      * - styles
		        - Additional CSS styles to apply to both the wrapper around the sidebar box as well as the content pane itself,
		          as a list of individual declarations (e.g. ``styles=["color: red", "display: block"]``) which will be joined
		          into the correct format by the template engine.
		      * - styles_link
		        - Like ``styles`` but only applied to the link in the navigation.
		      * - styles_content
		        - Like ``styles`` but only applied to the content pane itself.

		``settings`` type
		   .. figure:: ../images/template-plugin-type-settings.png
		      :align: center
		      :alt: Structure of settings plugins

		   Configures a settings component to inject. The value must be a dictionary, supported values are the following:

		   .. list-table::
		      :widths: 5 95

		      * - name
		        - The name under which to include the settings pane, if not set the name of the plugin will be used.
		      * - template
		        - Name of the template to inject, defaults to ``<pluginname>_settings.jinja2``.
		      * - suffix
		        - Suffix to attach to the element ID of the injected template, will be ``_<index>`` if not provided and not
		          the first template of the type, with ``index`` counting from 1 and increasing for each template of the same
		          type.
		      * - custom_bindings
		        - A boolean value indicating whether the default settings view model should be bound to the settings pane and link
		          in the navigation (``false``) or if a custom binding will be used by the plugin (``true``, default).
		      * - data_bind
		        - Additional knockout data bindings to apply to the template container, can be used to add further behaviour to
		          the container based on internal state if necessary.
		      * - classes
		        - Additional classes to apply to both the wrapper around the navigation link as well as the content pane itself, as a
		          list of individual classes (e.g. ``classes=["myclass", "myotherclass"]``) which will be joined into the correct
		          format by the template engine.
		      * - classes_link
		        - Like ``classes`` but only applied to the link in the navigation.
		      * - classes_content
		        - Like ``classes`` but only applied to the content pane itself.
		      * - styles
		        - Additional CSS styles to apply to both the wrapper around the navigation link as well as the content pane itself,
		          as a list of individual declarations (e.g. ``styles=["color: red", "display: block"]``) which will be joined
		          into the correct format by the template engine.
		      * - styles_link
		        - Like ``styles`` but only applied to the link in the navigation.
		      * - styles_content
		        - Like ``styles`` but only applied to the content pane itself

		``generic`` type
		   Configures a generic template to inject. The following keys are supported:

		   .. list-table::
		      :widths: 5 95

		      * - template
		        - Name of the template to inject, defaults to ``<pluginname>.jinja2``.

		.. note::

		   As already outlined above, each template type has a default template name (i.e. the default navbar template
		   of a plugin is called ``<pluginname>_navbar.jinja2``), which may be overridden using the template configuration.
		   If a plugin needs to include more than one template of a given type, it needs to provide an entry for each of
		   those, since the implicit default template will only be included automatically if no other templates of that
		   type are defined.

		:return list: a list containing the configuration options for the plugin's injected templates
		"""
		return []

	def get_template_vars(self):
		"""
		Defines additional template variables to include into the template renderer. Variable names will be prefixed
		with ``plugin_<plugin identifier>_``.

		:return dict: a dictionary containing any additional template variables to include in the renderer
		"""
		return dict()

	def get_template_folder(self):
		"""
		Defines the folder where the plugin stores its templates. Override this if your plugin stores its templates at
		some other place than the ``templates`` sub folder in the plugin base directory.

		:return string: the absolute path to the folder where the plugin stores its jinja2 templates
		"""
		import os
		return os.path.join(self._basefolder, "templates")


class SimpleApiPlugin(Plugin):
	def get_api_commands(self):
		return None

	def on_api_command(self, command, data):
		return None

	def on_api_get(self, request):
		return None


class BlueprintPlugin(Plugin):
	"""
	The ``BlueprintPlugin`` mixin allows plugins to define their own full fledged endpoints for whatever purpose,
	be it a more sophisticated API than what is possible via the :class:`SimpleApiPlugin` or a custom web frontend.

	The mechanism at work here is `Flask's <http://flask.pocoo.org/>`_ own `Blueprint mechanism <http://flask.pocoo.org/docs/0.10/blueprints/>`_.

	The mixin automatically creates a blueprint for you that will be registered under ``/plugin/<plugin identifier>/``.
	All you need to do is decorate all of your view functions with the :func:`route` decorator,
	which behaves exactly the same like Flask's regular ``route`` decorators. Example:

	.. code-block:: python
	   :linenos:

	   import octoprint.plugin
	   import flask

	   class MyBlueprintPlugin(octoprint.plugin.BlueprintPlugin):
	       @octoprint.plugin.BlueprintPlugin.route("/echo", methods=["GET"])
	       def myEcho(self):
	           if not "text" in flask.request.values:
	               return flask.make_response("Expected a text to echo back.", 400)
	           return flask.request.values["text"]

	   __plugin_implementations__ = [MyPlugin()]

	Your blueprint will be published by OctoPrint under the base URL ``/plugin/<plugin identifier>/``, so the above
	example of a plugin with the identifier "myblueprintplugin" would be reachable under
	``/plugin/myblueprintplugin/echo``.

	Just like with regular blueprints you'll be able to create URLs via ``url_for``, just use the prefix
	``plugin.<plugin identifier>``, e.g.:

	.. code-block:: python

	   flask.url_for("plugin.myblueprintplugin.echo") # will return "/plugin/myblueprintplugin/echo"

	"""

	@staticmethod
	def route(rule, **options):
		"""
		A decorator to mark view methods in your BlueprintPlugin subclass. Works just the same as Flask's
		own ``route`` decorator available on blueprints.

		See `the documentation for flask.Blueprint.route <http://flask.pocoo.org/docs/0.10/api/#flask.Blueprint.route>`_
		and `the documentation for flask.Flask.route <http://flask.pocoo.org/docs/0.10/api/#flask.Flask.route>`_ for more
		information.
		"""

		from collections import defaultdict
		def decorator(f):
			# We attach the decorator parameters directly to the function object, because that's the only place
			# we can access right now.
			# This neat little trick was adapter from the Flask-Classy project: https://pythonhosted.org/Flask-Classy/
			if not hasattr(f, "_blueprint_rules") or f._blueprint_rules is None:
				f._blueprint_rules = defaultdict(list)
			f._blueprint_rules[f.__name__].append((rule, options))
			return f
		return decorator

	def get_blueprint(self):
		"""
		Creates and returns the blueprint for your plugin. Override this if you want to define and handle your blueprint yourself.

		This method will only be called once during server initialization.

		:return: the blueprint ready to be registered with Flask
		"""

		import flask
		blueprint = flask.Blueprint("plugin." + self._identifier, self._identifier)
		for member in [member for member in dir(self) if not member.startswith("_")]:
			f = getattr(self, member)
			if hasattr(f, "_blueprint_rules") and member in f._blueprint_rules:
				for blueprint_rule in f._blueprint_rules[member]:
					rule, options = blueprint_rule
					blueprint.add_url_rule(rule, options.pop("endpoint", f.__name__), view_func=f, **options)
		return blueprint

	def is_blueprint_protected(self):
		"""
		Whether a valid API key is needed to access the blueprint (the default) or not.
		"""

		return True


class SettingsPlugin(Plugin):
	"""
	Including the ``SettingsPlugin`` mixin allows plugins to store and retrieve their own settings within OctoPrint's
	configuration.

	Plugins including the mixing will get injected an additional property ``self._settings`` which is an instance of
	:class:`PluginSettingsManager` already properly initialized for use by the plugin. In order for the manager to
	know about the available settings structure and default values upon initialization, implementing plugins will need
	to provide a dictionary with the plugin's default settings through overriding the method :func:`get_settings_defaults`.
	The defined structure will then be available to access through the settings manager available as ``self._settings``.

	If your plugin needs to react to the change of specific configuration values on the fly, e.g. to adjust the log level
	of a logger when the user changes a corresponding flag via the settings dialog, you can override the
	:func:`on_settings_save` method and wrap the call to the implementation from the parent class with retrieval of the
	old and the new value and react accordingly.

	Example:

	.. code-block:: python

	   import octoprint.plugin

	   class MySettingsPlugin(octoprint.plugin.SettingsPlugin, octoprint.plugin.StartupPlugin):
	       def get_settings_defaults(self):
	           return dict(
	               some_setting="foo",
	               some_value=23,
	               sub=dict(
	                   some_flag=True
	               )
	           )

	       def on_settings_save(self, data):
	           old_flag = self._settings.getBoolean(["sub", "some_flag"])

	           super(MySettingsPlugin, self).on_settings_save(data)

	           new_flag = self._settings.getBoolean(["sub", "some_flag"])
	           if old_flag != new_flag:
	               self._logger.info("sub.some_flag changed from {old_flag} to {new_flag}".format(**locals()))

	       def on_after_startup(self):
	           some_setting = self._settings.get(["some_setting"])
	           some_value = self._settings.getInt(["some_value"])
	           some_flag = self._settings.getBoolean(["sub", "some_flag"])
	           self._logger.info("some_setting = {some_setting}, some_value = {some_value}, sub.some_flag = {some_flag}".format(**locals())

	   __plugin_implementations__ = [MySettingsPlugin()]

	Of course, you are always free to completely override both :func:`on_settings_load` and :func:`on_settings_save` if the
	default implementations do not fit your requirements.
	"""

	def on_settings_load(self):
		"""
		Loads the settings for the plugin, called by the Settings API view in order to retrieve all settings from
		all plugins. Override this if you want to inject additional settings properties that are not stored within
		OctoPrint's configuration.

		.. note::

		   The default implementation will return your plugin's settings as is, so just in the structure and in the types
		   that are currently stored in OctoPrint's configuration.

		   If you need more granular control here, e.g. over the used data types, you'll need to override this method
		   and iterate yourself over all your settings, using the proper retriever methods on the settings manager
		   to retrieve the data in the correct format.

		:return: the current settings of the plugin, as a dictionary
		"""
		return self._settings.get([], asdict=True, merged=True)

	def on_settings_save(self, data):
		"""
		Saves the settings for the plugin, called by the Settings API view in order to persist all settings
		from all plugins. Override this if you need to directly react to settings changes or want to extract
		additional settings properties that are not stored within OctoPrint's configuration.

		.. note::

		   The default implementation will persist your plugin's settings as is, so just in the structure and in the
		   types that were received by the Settings API view.

		   If you need more granular control here, e.g. over the used data types, you'll need to override this method
		   and iterate yourself over all your settings, retrieving them (if set) from the supplied received ``data``
		   and using the proper setter methods on the settings manager to persist the data in the correct format.

		:param dict data: the settings dictionary to be saved for the plugin
		"""
		import octoprint.util

		current = self._settings.get([], asdict=True, merged=True)
		data = octoprint.util.dict_merge(current, data)
		self._settings.set([], data)

	def get_settings_defaults(self):
		"""
		Retrieves the plugin's default settings with which the plugin's settings manager will be initialized.

		Override this in your plugin's implementation and return a dictionary defining your settings data structure
		with included default values.
		"""
		return dict()


class EventHandlerPlugin(Plugin):
	def on_event(self, event, payload):
		pass


class SlicerPlugin(Plugin):
	def is_slicer_configured(self):
		return False

	def get_slicer_properties(self):
		return dict(
			type=None,
			name=None,
			same_device=True,
			progress_report=False
		)

	def get_slicer_profile_options(self):
		return None

	def get_slicer_profile(self, path):
		return None

	def get_slicer_default_profile(self):
		return None

	def save_slicer_profile(self, path, profile, allow_overwrite=True, overrides=None):
		pass

	def do_slice(self, model_path, printer_profile, machinecode_path=None, profile_path=None, on_progress=None, on_progress_args=None, on_progress_kwargs=None):
		pass

	def cancel_slicing(self, machinecode_path):
		pass


class ProgressPlugin(Plugin):
	"""
	Via the ``ProgressPlugin`` mixing plugins can let themselves be called upon progress in print jobs or slicing jobs,
	limited to minimally 1% steps.
	"""

	def on_print_progress(self, storage, path, progress):
		"""
		Called by OctoPrint on minimally 1% increments during a running print job.

		:param string location: Location of the file
		:param string path:     Path of the file
		:param int progress:    Current progress as a value between 0 and 100
		"""
		pass

	def on_slicing_progress(self, slicer, source_location, source_path, destination_location, destination_path, progress):
		"""
		Called by OctoPrint on minimally 1% increments during a running slicing job.

		:param string slicer:               Key of the slicer reporting the progress
		:param string source_location:      Location of the source file
		:param string source_path:          Path of the source file
		:param string destination_location: Location the destination file
		:param string destination_path:     Path of the destination file
		:param int progress:                Current progress as a value between 0 and 100
		"""
		pass


class AppPlugin(Plugin):
	def get_additional_apps(self):
		return []

