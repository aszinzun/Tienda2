var total=0;
function seleccionarProducto(id,cantidad,precio){

    if(document.getElementById(id).checked){
        //alert(id+","+(cantidad*precio));
        total+=cantidad*precio;

    }
    else{
        total-=cantidad*precio;
    }
    document.getElementById("total").value=total;
}