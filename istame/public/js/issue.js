// cur_frm.fields_dict.sub_category.get_query = function (doc) {
//     return {
//         filters: {
//             "contact_type": doc.contact_type      
//         }
//     }
// };
// frappe.ui.form.on('Issue', {
//     before_save: function(frm){
// 		if(!frm.doc.__islocal && !frm.doc.subject.includes(frm.doc.name)){
// 			frm.set_value('subject', frm.doc.subject + ":" + frm.doc.name);
// 		}
//         frm.trigger('service_type')
// 	},
//     service_type: function(frm){
//         frm.set_value("zone",'');
//         frm.set_value("service_provider_name",'');
//         frm.set_value("area",'');
//         frm.set_value("sp_email_addresses",'');
//         frm.set_value("contact_name_1",'');
//         frm.set_value("contact_number_1",'');
//         frm.set_value("contact_name_2",'');
//         frm.set_value("contact_number_2",'');
//         if(frm.doc.building_name && frm.doc.service_type){
//             frappe.call({
//                 'method': "hoam.api.get_building_detail",
//                 'args':{
//                     'building_name': frm.doc.building_name,
//                     'service_type': frm.doc.service_type
//                 },
//                 callback: function(r){
//                     if(r.message){
//                         frappe.model.with_doc("Building", r.message[0].name, function() {
//                             var building = frappe.model.get_doc("Building", r.message[0].name);
//                             frm.set_value("zone",building.zone);
//                             frm.set_value("service_provider_name",building.service_provider_name);
//                             frm.set_value("area",building.area);
//                             frm.set_value("sp_email_addresses",building.sp_email_addresses);
//                             frm.set_value("contact_name_1",building.contact_name_1);
//                             frm.set_value("contact_number_1",building.contact_number_1);
//                             frm.set_value("contact_name_2",building.contact_name_2);
//                             frm.set_value("contact_number_2",building.contact_number_2);
                            
//                         });
//                     }
//                     else{
//                         frm.set_value("zone",'');
//                         frm.set_value("service_provider_name",'');
//                         frm.set_value("area",'');
//                         frm.set_value("sp_email_addresses",'');
//                         frm.set_value("contact_name_1",'');
//                         frm.set_value("contact_number_1",'');
//                         frm.set_value("contact_name_2",'');
//                         frm.set_value("contact_number_2",'');
//                     }
//                 }
//             })
//         }
//     }
// });



