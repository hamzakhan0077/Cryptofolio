const ListItem = props => {
  const listItem = React.useRef();
  React.useEffect(function () {
    props.passRefUpward(listItem, props.id);
  });

  const clicked = () => {
    console.log("clicked");
    console.log(props.url);
    window.location.href = props.url;
  };

  return /*#__PURE__*/React.createElement("div", {
    className: "listitem",
    ref: listItem // style={{
    //     width:`${props.unSelectedSize}px`, 
    //     height:`${props.unSelectedSize}px`
    //     }}
    ,
    styel: {
      width: "fit-content"
    }
  }, /*#__PURE__*/React.createElement("img", {
    className: "image",
    src: props.img,
    alt: `nft for ${props.nft_name}`,
    onDragStart: e => e.preventDefault(),
    onDoubleClick: clicked
  }), /*#__PURE__*/React.createElement("div", {
    className: "bottom"
  }, /*#__PURE__*/React.createElement("span", {
    className: "collection_name"
  }, props.collection_name), /*#__PURE__*/React.createElement("div", {
    className: "price"
  }, /*#__PURE__*/React.createElement("span", {
    className: "count"
  }, props.count), /*#__PURE__*/React.createElement("span", null, " NFTs"))));
};

export default ListItem;