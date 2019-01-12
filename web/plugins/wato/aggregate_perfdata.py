#!/usr/bin/python
# Copyright 2018, 2019 comNET GmbH
#
# This file is part of aggregate_perfdata.
#
# aggregate_perfdata is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as published by
# the Free Software Foundation.
#
# aggregate_perfdata is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with aggregate_perfdata.  If not, see <https://www.gnu.org/licenses/>.

class UnitChoice(DropdownChoice):
    def __init__(self, **args):
        DropdownChoice.__init__(self,
            title = _("Unit"),
            choices = self._unit_choices,
            **args)

    def _unit_choices(self):
        from metrics import unit_info
        return sorted([
            (name, info.get("description", info["title"])) for
             (name, info) in unit_info.items()],
             cmp = lambda a,b: cmp(a[1], b[1]))

group = "datasource_programs"
register_rule(group,
    "special_agents:aggregate_perfdata",
    Dictionary(
         elements = [
             ("description",
                 TextAscii(
                     title = _("Service Description"),
                     default_value = _("Aggregated Performance Data"),
                 )
             ),
             ("hosts",
                 TextAscii(
                     title = _("Filter hosts via regex"),
                     help = _("You can enter $HOSTNAME$ to use the host that the service is running on"),
                 )
             ),
             ("host_group",
                  GroupSelection(
                      "host",
                      title = _("Filter hosts via host group"),
                  )
              ),
             ("services",
                 TextAscii(
                     title = _("Filter services via regex"),
                 )
             ),
             ("service_group",
                 GroupSelection(
                     "service",
                     title = _("Filter services via service group"),
                 )
             ),
             ("replace_by_index", ListOf(Tuple(
                orientation = "horizontal",
                elements = [
                    Integer(
                        title = _("Variable index"),
                    ),
                    TextAscii(
                        title = _("New perfdata variable name"),
                    )
                ]),
                title = _('Replace perfdata variable names by index'),
             )),
             ("disable_by_index", ListOf(Tuple(
                orientation = "horizontal",
                elements = [
                    Integer(
                        title = _("Variable index"),
                        help = _("Disable specific perfdata variables"),
                    ),
                ]),
                title = _('Disable perfdata variables by index'),
             )),
             ("map_metrics", ListOf(Tuple(
                orientation = "horizontal",
                elements = [
                    TextAscii(
                        title = _("Metric name"),
                    ),
                    UnitChoice(),
                    TextAscii(
                        title = _("Display name"),
                    ),
                    Float(
                        title = _("Scaling"),
                        size = 20,
                        default_value = 1
                    ),
                ]),
                title = _('Map metric information (unit, display name, scaling)'),
             )),
             ("algorithm",
                 DropdownChoice( title = _("Algorithm"),
                     choices = [ ("sum", _("Sum")), ("average", _("Average")) ],
                 ),
             ),
         ],
        required_keys = ["algorithm", "description"]
    ),
    title = _("Aggregate performance data"),
    match = "first"
)
