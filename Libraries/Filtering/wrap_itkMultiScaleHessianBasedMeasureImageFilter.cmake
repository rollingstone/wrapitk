WRAP_CLASS("itk::MultiScaleHessianBasedMeasureImageFilter" POINTER)
  FOREACH(d ${WRAP_ITK_DIMS})
    FOREACH(t ${WRAP_ITK_SCALAR})
      WRAP_TEMPLATE("${ITKM_I${t}${d}}${ITKM_ISSRTD${d}${d}}${ITKM_I${t}${d}}" "${ITKT_I${t}${d}}, ${ITKT_ISSRTD${d}${d}}, ${ITKT_I${t}${d}}")
    ENDFOREACH(t)
  ENDFOREACH(d)
END_WRAP_CLASS()
