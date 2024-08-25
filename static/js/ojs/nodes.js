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
            d.search = $('#node_search').val();
        }
    },

    columns: [
        {data: 'id', name: 'id',title: '#',orderable: true,width:'4%'},
        {data: 'ip', name: 'ip',orderable: true},
        {data: 'name', name: 'name',orderable: true},
        {data: 'vm', name: 'vm',orderable: true},
        {data: 'storage', name: 'storage',orderable: false},
        {data: 'ram', name: 'ram',orderable: false},
        {data: 'note', name: 'note',orderable: false},
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
$('#user_filter').change(function (e) {
    userTable.page.len($(this).val()).draw();
});

$('#node_search').keyup(function (e) {
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
} );

jQuery(function(){
    var m=document.getElementById('NodeModel'),table=document.getElementById('NodeTable');
    var nodes = {
        init: function() {
            jQuery(document).on('click','.btn-submit',function(e){
                //jQuery('.pre-loader').show();
                var _this = jQuery(this);
                e.preventDefault();
                nodes.fire(_this,"save");
            });
            jQuery(document).on('click','.fill_data',function(e){
                //jQuery('.pre-loader').show();
                var _this = jQuery(this);
                e.preventDefault();
                nodes.fire(_this,"fetch");
            });
            jQuery(document).on('click',".btn-delete",function(e){
                //jQuery('.pre-loader').show();
                var _this = jQuery(this);
                e.preventDefault();
                if(confirm('Are you sure?')){
                    nodes.fire(_this,"delete");
                }
            });

            $(document).on('click','.show_password', function(event) {
                event.preventDefault();
                var parent = $(this).parent('td');
                if($(parent).find('.show_password i').hasClass("fa fa-eye-slash"))
                {
                    jQuery.get(jQuery(this).data('url'),function(response){
                        $(parent).find(".text").html(response);
                    });
                }
                $(parent).find(".password").toggle();
                $(parent).find(".text").toggle();
                $(parent).find('.show_password i').toggleClass( "fa-eye-slash" );
                $(parent).find('.show_password i').toggleClass( "fa-eye" );
            });

            $(document).ready(function() {
                $(window).keydown(function(event){
                  if(event.keyCode == 13) {
                    event.preventDefault();
                    return false;
                  }
                });
            });
        },
        fire: function(_this,action) {
            var _f = _this.parents('form');
            var method = action == "save" ? _f.attr('method') : _this.data('method');
            var url = action == "save" ? _f.attr('action') : _this.data('url');
            var data = action == "delete" ? {_token: jQuery('meta[name="csrf-token"]').attr('content')} : _f.serialize();
            var ajax = {
                fire: function(){
                    $.ajax({
                        type: method,
                        url: url,
                        data: data,
                    })
                    .done(function(response) {
                        ajax.success(response)
                    })
                    .fail(function(response) {
                        ajax.error(response)
                    });
                },
                success: function(response){
                    //jQuery('.pre-loader').hide();
                    userTable.ajax.reload();

                    if(action == "fetch")
                    {
                        jQuery(".modal-content").html(response);
                        jQuery(m).modal('show');
                    }
                    else if(action == "delete")
                    {
                        jQuery(_this).parents("tr").remove();
                        jQuery(m).modal('hide');
                    }
                    else if(action == "save")
                    {
                        jQuery(m).modal('hide');
                    }

                },
                error: function(error){
                    jQuery('.pre-loader').hide();
                    jQuery(_f).find(".has-error").remove();
                    var response = JSON.parse(error.responseText);
                    $.each(error.responseJSON, function (key, value) {
                        if(key == 'agree_terms')
                        {
                            jQuery('.confirm-read-tc').find('.has-error').remove();
                            jQuery('.confirm-read-tc').append("<span class='has-error'>"+ value +"</span>");
                        }
                        else
                        {
                            var input = '[name=' + key + ']';
                            jQuery(_f).find(input).parent().find(".has-error").length == 0 ? jQuery(_f).find(input).parent().append("<span class='has-error'>"+ value +"</span>") : jQuery(_f).find(input).parent().find('.has-error').html(value);
                        }
                    });
                }
            }
            ajax.fire();
        }
    }

    var model = {
        init: function(){
            jQuery(m).on('shown.bs.modal',function(){
            });
            jQuery(m).on('hidden.bs.modal', function(){
                jQuery(this).find('form')[0].reset();
                jQuery(this).find('.has-error').remove();
                //jQuery.get('/do_rollback',function(){});
            });
        }
    }
    nodes.init();
    model.init();
});
