/* Define two custom functions (asc and desc) for string sorting */
jQuery.fn.dataTableExt.oSort['string-case-asc']  = function(x,y) {
	return ((x < y) ? -1 : ((x > y) ?  1 : 0));
};

jQuery.fn.dataTableExt.oSort['string-case-desc'] = function(x,y) {
	return ((x < y) ?  1 : ((x > y) ? -1 : 0));
};
var userTable = $('#NodeTable').DataTable({
    dom: '<"top">tr<"bottom"ip>',
    processing: true,
    serverSide: true,
    pageLength: 10,
    searching: true,
    ajax: {
        url: list,
        data: function (d) {
            d.search = jQuery('#node_search').val();
            d.node_type=jQuery('#node_type').val();
            d.main_node_id=jQuery('#main_node_id').val();
            d.rack_no = jQuery("#rack_no").val();
            d.rack_position_id = jQuery("#rack_position").val();
            d.operating_system_id = jQuery("#operating_system").val();
            d.virtual_type_id = jQuery("#virtual_type").val();
            d.location_id = jQuery("#location").val();
            d.vlan = jQuery("#vlan").val();
            d.status = jQuery("#status").val();
            d.date_range = jQuery("#setup_date").val();
            d.min_ram = jQuery("#min_ram").val();
            d.max_ram = jQuery("#max_ram").val();
            d.min_ram = jQuery("#min_cores").val();
            d.max_ram = jQuery("#max_cores").val();

        }
    },

    columns: [
        {data: 'id', name: 'id',title: '#',orderable: true,width:'4%'},
        {data: 'ip', name: 'ip',orderable: true},
        {data: 'name', name: 'name',orderable: true},
        {data: 'vm', name: 'vm',orderable: true},
        {data: 'main_node', name: 'main_node',orderable: false},
        {data: 'action', name: 'action', orderable: false,width:'10%'},
    ],
    language: {
        emptyTable: "No matching records found"
    },
    fnDrawCallback: function(oSettings) {
        // Hide pagination when data is less then pagelimit
        if (oSettings._iDisplayLength > oSettings.fnRecordsDisplay()) {
            $(oSettings.nTableWrapper).find('.dataTables_paginate').hide();
        }
        else{
            $(oSettings.nTableWrapper).find('.dataTables_paginate').show();
        }
        $('[data-toggle="tooltip"]').tooltip();
    }
});

/* Custom Filter*/
$('.custom_filter').change(function (e) {
    userTable.draw();
});

$('.custom_search').keyup(function (e) {
    userTable.draw();
});

// Sort by columns 1 and 2 and redraw
userTable.order( [ 0, 'desc' ]).draw();

$.fn.dataTable.ext.errMode = 'none';
userTable.on('error', function () {
    alert("Something went wrong, Please try after sometimes.");
});

$('#NodeTable_wrapper tbody').on('click', '.node_details', function () {
    var tr = $(this).closest('tr');
    var _url = $(this).data('href');
    var row = userTable.row( tr );
    if ( row.child.isShown() ) {
        // This row is already open - close it
        $('div.node_data_details', row.child()).slideUp( function () {
            row.child.hide();
            tr.removeClass('shown');
        } );
        $(tr).find('.node_details i').removeClass('fa-minus-square').addClass('fa-plus-square');
    }
    else {
        // Open this row
        $.get(_url,function(response){
            row.child( response, 'no-padding' ).show();
            tr.addClass('shown');
            $(tr).find('.node_details i').removeClass('fa-plus-square').addClass('fa-minus-square');
            $('div.node_data_details', row.child()).slideDown();
        });
    }
} );



$('#NodeTable_wrapper tbody').on('click', '.vm_nodes', function () {
    var tr = $(this).closest('tr');
    var _url = $(this).data('href');
    var row = userTable.row( tr );
    if ( row.child.isShown() ) {
        // This row is already open - close it
        $('div.vm_nodes_slide', row.child()).slideUp( function () {
            row.child.hide();
            tr.removeClass('shown');
        } );
        $(tr).find('.vm_nodes i').removeClass('fa-minus-square').addClass('fa-plus-square');
    }
    else {
        // Open this row
        $.get(_url,function(response){
            row.child( response, 'no-padding' ).show();
            tr.addClass('shown');

            $('div.vm_nodes_slide', row.child()).slideDown();
            $(tr).find('.vm_nodes i').removeClass('fa-plus-square').addClass('fa-minus-square');
        });
    }
} );

$('#NodeTable_wrapper tbody').on('click', '.note_list', function () {
    var tr = $(this).closest('tr');
    var _url = $(this).data('href');
    var row = userTable.row( tr );
    if ( row.child.isShown() ) {
        // This row is already open - close it
        $('div.note_list', row.child()).slideUp( function () {
            row.child.hide();
            tr.removeClass('shown');
        } );
        $(tr).find('.note_list i').removeClass('fa-minus-square').addClass('fa-plus-square');
    }
    else {
        // Open this row
        $.get(_url,function(response){
            row.child( response, 'no-padding' ).show();
            tr.addClass('shown');

            $('div.note_list', row.child()).slideDown();
            $(tr).find('.note_list i').removeClass('fa-plus-square').addClass('fa-minus-square');
        });
    }
});