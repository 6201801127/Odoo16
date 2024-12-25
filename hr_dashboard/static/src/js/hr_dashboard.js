odoo.define('hr_dashboard.hr_dashboard', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;

    var HrDashboard = AbstractAction.extend({
        // Start function that triggers when the action is loaded
        start: function () {
            var self = this;
            // self.load_data();
            var self = this;
            self._rpc({
                model: 'hr.employee',
                method: 'fetch_emp_data',
            }).then(function (result) {
                // console.log("Data received=============:", result[0]['id']);
                // Rendering the template with the data received
                $(".o_menu_apps").find('.dropdown-menu[role="menu"]').removeClass("show");

                self.$el.html(QWeb.render('hr_dashboard_temp_id', {
                    report_lines: result,
                }));
            });
        },
    });

    // Register the action
    core.action_registry.add("hr_dashboard_action_tag", HrDashboard);
    return HrDashboard;
});
