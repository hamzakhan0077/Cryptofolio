const ListItem = props => {
  const listItem = React.useRef();
  React.useEffect(function () {
    props.passRefUpward(listItem, props.id);
  });
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
    onDragStart: e => e.preventDefault()
  }), /*#__PURE__*/React.createElement("span", {
    className: "nft_name"
  }, props.nft_name), /*#__PURE__*/React.createElement("span", {
    className: "owner"
  }, props.owner), /*#__PURE__*/React.createElement("div", {
    className: "buy"
  }, /*#__PURE__*/React.createElement("a", {
    className: "button",
    href: "buy"
  }, "Buy "), /*#__PURE__*/React.createElement("span", {
    className: "price"
  }, props.price)));
};

export default ListItem;