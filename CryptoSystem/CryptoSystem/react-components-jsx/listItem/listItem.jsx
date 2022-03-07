const ListItem = (props) => {
    let size;

    if(props.selected) {
        size = props.selectedSize
    } else {
        size = props.unSelectedSize
    }
    return (
        <div className="listitem"
            style={{
                width:`${size}px`, 
                height:`${size}px`
                }}
        >

            <img className="image" 
                src={props.img} 
                alt={`nft for ${props.nft_name}`}
                onDragStart={(e) => e.preventDefault()}
            /> 

            <span className="nft_name">{props.nft_name}</span>
            <span className="owner">{props.owner}</span>
        </div>
    )
}

export default ListItem