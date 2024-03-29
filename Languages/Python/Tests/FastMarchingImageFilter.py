
#     INPUTS: BrainProtonDensitySlice.png
#     OUTPUTS: FastMarchingImageFilterOutput5.png
#     81 114 1.0  -0.5  3.0   100 100
#
#     INPUTS: BrainProtonDensitySlice.png
#     OUTPUTS: FastMarchingImageFilterOutput6.png
#     99 114 1.0  -0.5  3.0   100 100
#
#     INPUTS: BrainProtonDensitySlice.png
#     OUTPUTS: FastMarchingImageFilterOutput7.png
#     56 92 1.0  -0.3  2.0   200 100
#
#     INPUTS: BrainProtonDensitySlice.png
#     OUTPUTS: FastMarchingImageFilterOutput8.png
#     OUTPUTS: [FastMarchingFilterOutput1.png]
#     OUTPUTS: [FastMarchingFilterOutput2.png]
#     OUTPUTS: [FastMarchingFilterOutput3.png]
#     40 90 0.5  -0.3  2.0   200 100

import itk
from sys import argv, stderr, exit


if( len(argv) < 10 ):
  print >> stderr, """Missing Parameters
Usage: FastMarchingImageFilter.py inputImage  outputImage seedX seedY Sigma SigmoidAlpha SigmoidBeta TimeThreshold StoppingValue"""
  exit(1)

itk.auto_progress(2)


InternalPixelType = itk.F
Dimension = 2
InternalImageType = itk.Image[ InternalPixelType, Dimension ]

OutputPixelType = itk.UC
OutputImageType = itk.Image[ OutputPixelType, Dimension ]

thresholder = itk.BinaryThresholdImageFilter[ InternalImageType, OutputImageType ].New();

timeThreshold = float( argv[8] )
thresholder.SetLowerThreshold(           0.0  )
thresholder.SetUpperThreshold( timeThreshold  )

thresholder.SetOutsideValue(  0  )
thresholder.SetInsideValue(  255 )

ReaderType = itk.ImageFileReader[ InternalImageType ]
WriterType = itk.ImageFileWriter[ OutputImageType ]

reader = ReaderType.New()
writer = WriterType.New()

reader.SetFileName( argv[1] )
writer.SetFileName( argv[2] )


CastFilterType = itk.RescaleIntensityImageFilter[
                            InternalImageType,
                            OutputImageType ]

SmoothingFilterType = itk.CurvatureAnisotropicDiffusionImageFilter[
                            InternalImageType,
                            InternalImageType ]

smoothing = SmoothingFilterType.New()

GradientFilterType = itk.GradientMagnitudeRecursiveGaussianImageFilter[
                            InternalImageType,
                            InternalImageType ]

SigmoidFilterType = itk.SigmoidImageFilter[
                            InternalImageType,
                            InternalImageType ]

gradientMagnitude = GradientFilterType.New();
sigmoid = SigmoidFilterType.New()

sigmoid.SetOutputMinimum(  0.0  )
sigmoid.SetOutputMaximum(  1.0  )

FastMarchingFilterType = itk.FastMarchingImageFilter[ InternalImageType,
                            InternalImageType ]

fastMarching = FastMarchingFilterType.New()

smoothing.SetInput( reader.GetOutput() )
gradientMagnitude.SetInput( smoothing.GetOutput() )
sigmoid.SetInput( gradientMagnitude.GetOutput() )
fastMarching.SetInput( sigmoid.GetOutput() )
thresholder.SetInput( fastMarching.GetOutput() )
writer.SetInput( thresholder.GetOutput() )

smoothing.SetTimeStep( 0.125 )
smoothing.SetNumberOfIterations(  5 )
smoothing.SetConductanceParameter( 9.0 )

sigma = float( argv[5] )

gradientMagnitude.SetSigma(  sigma  )

alpha =  float( argv[6] )
beta  =  float( argv[7] )

sigmoid.SetAlpha( alpha )
sigmoid.SetBeta(  beta  )

NodeType = itk.LevelSetNode[InternalPixelType, Dimension]
NodeContainer = itk.VectorContainer[itk.UI, NodeType]
seeds = NodeContainer.New()

seedPosition = [int( argv[3] ), int( argv[4] )]


node = NodeType()
seedValue = 0.0

node.SetValue( seedValue )
node.SetIndex( seedPosition )

seeds.Initialize();
seeds.InsertElement( 0, node )

fastMarching.SetTrialPoints(  seeds  );

caster1 = CastFilterType.New()
caster2 = CastFilterType.New()
caster3 = CastFilterType.New()
caster4 = CastFilterType.New()

writer1 = WriterType.New()
writer2 = WriterType.New()
writer3 = WriterType.New()
writer4 = WriterType.New()

caster1.SetInput( smoothing.GetOutput() )
writer1.SetInput( caster1.GetOutput() )
writer1.SetFileName("FastMarchingFilterOutput1.png")
caster1.SetOutputMinimum(   0 )
caster1.SetOutputMaximum( 255 )
writer1.Update()

caster2.SetInput( gradientMagnitude.GetOutput() )
writer2.SetInput( caster2.GetOutput() )
writer2.SetFileName("FastMarchingFilterOutput2.png")
caster2.SetOutputMinimum(   0 )
caster2.SetOutputMaximum( 255 )
writer2.Update()

caster3.SetInput( sigmoid.GetOutput() )
writer3.SetInput( caster3.GetOutput() )
writer3.SetFileName("FastMarchingFilterOutput3.png")
caster3.SetOutputMinimum(   0 )
caster3.SetOutputMaximum( 255 )
writer3.Update()

caster4.SetInput( fastMarching.GetOutput() )
writer4.SetInput( caster4.GetOutput() )
writer4.SetFileName("FastMarchingFilterOutput4.png")
caster4.SetOutputMinimum(   0 )
caster4.SetOutputMaximum( 255 )


fastMarching.SetOutputSize(
        reader.GetOutput().GetBufferedRegion().GetSize() )

stoppingTime = float( argv[9] )

fastMarching.SetStoppingValue(  stoppingTime  )

writer.Update()


writer4.Update()


InternalWriterType = itk.ImageFileWriter[ InternalImageType ]

mapWriter = InternalWriterType.New()
mapWriter.SetInput( fastMarching.GetOutput() )
mapWriter.SetFileName("FastMarchingFilterOutput4.mha")
mapWriter.Update()

speedWriter = InternalWriterType.New()
speedWriter.SetInput( sigmoid.GetOutput() )
speedWriter.SetFileName("FastMarchingFilterOutput3.mha")
speedWriter.Update()

gradientWriter = InternalWriterType.New()
gradientWriter.SetInput( gradientMagnitude.GetOutput() )
gradientWriter.SetFileName("FastMarchingFilterOutput2.mha")
gradientWriter.Update()
