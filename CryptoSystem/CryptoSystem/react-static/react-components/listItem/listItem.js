const ListItem = props => {
  let size;

  if (props.selected) {
    size = props.selectedSize;
  } else {
    size = props.unSelectedSize;
  }

  return /*#__PURE__*/React.createElement("div", {
    className: "listitem",
    style: {
      width: `${size}px`,
      height: `${size}px`
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
  }, props.owner));
};

export default ListItem;