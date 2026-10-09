export function errorHandler(err, req, res, next) {
  console.error('❌ Server Error:', err.message);

  if (err.name === 'MulterError') {
    if (err.code === 'LIMIT_FILE_SIZE') {
      return res.status(413).json({
        success: false,
        error: 'File size limit exceeded. Maximum allowed file size is 25MB.',
        code: 'FILE_TOO_LARGE'
      });
    }
    return res.status(400).json({
      success: false,
      error: `Upload error: ${err.message}`,
      code: 'UPLOAD_ERROR'
    });
  }

  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    success: false,
    error: err.message || 'Internal server error occurred.',
    code: err.code || 'INTERNAL_ERROR'
  });
}
