function ImageUploader({ setImageUrl, resetStates }) {
  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const url = URL.createObjectURL(file);
    setImageUrl(url);
    resetStates();
  };

  return (
    <input
      type="file"
      accept="image/*"
      onChange={handleUpload}
      className="file-input"
    />
  );
}

export default ImageUploader;
