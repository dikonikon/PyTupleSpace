/*

Adapted from example grid panel in extjs 4 distribution

*/
Ext.require([
'Ext.grid.*',
'Ext.data.*',
'Ext.util.*',
'Ext.state.*',
'Ext.button.*'
]);

Ext.onReady(function() {
    Ext.QuickTips.init();

    // setup the state provider, all state information will be saved to a cookie
    Ext.state.Manager.setProvider(Ext.create('Ext.state.CookieProvider'));

    // sample static data for the store
    var myData = [
        ['none']
    ];

    /**
     * Custom function used for column renderer
     * @param {Object} val
     */
    function change(val) {
        if (val > 0) {
            return '<span style="color:green;">' + val + '</span>';
        } else if (val < 0) {
            return '<span style="color:red;">' + val + '</span>';
        }
        return val;
    }

    /**
     * Custom function used for column renderer
     * @param {Object} val
     */
    function pctChange(val) {
        if (val > 0) {
            return '<span style="color:green;">' + val + '%</span>';
        } else if (val < 0) {
            return '<span style="color:red;">' + val + '%</span>';
        }
        return val;
    }

    // create the data store
    var store = Ext.create('Ext.data.ArrayStore', {
        fields: [
           {name: 'textline'}
                ],
        data: myData
    });

    // create the Grid
    var grid = Ext.create('Ext.grid.Panel', {
        store: store,
        stateful: true,
        stateId: 'stateGrid',
        columns: [
            {
                text     : 'Random Text Line',
                flex     : 1,
                sortable : true,
                dataIndex: 'textline'
            }
        ],
        height: 350,
        width: 600,
        title: 'Ipso Data',
        renderTo: 'ipso-panel',
        viewConfig: {
            stripeRows: true
        }
    });


    Ext.create('Ext.Button', {
            text: 'Get Random Text',
            renderTo: 'ipso-button',
            handler: getDataDoClick
            }
    );

    function getDataDoClick() {
            alert("clicked!");
        }

});



