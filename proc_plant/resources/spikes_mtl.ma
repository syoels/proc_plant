//Maya ASCII 2019 scene
//Name: spikes_mtl.ma
//Last modified: Wed, Mar 31, 2021 08:06:16 PM
//Codeset: 1255
requires maya "2019";
requires -nodeType "aiStandardSurface" -nodeType "aiColorCorrect" "mtoa" "3.1.2";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2019";
fileInfo "version" "2019";
fileInfo "cutIdentifier" "201812112215-434d8d9c04";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 18363)\n";
fileInfo "license" "student";
createNode aiStandardSurface -n "spikes_mtl";
	rename -uid "845A1ED2-473D-4432-7F51-4E8DB16F7712";
	setAttr ".base" 0.7622377872467041;
	setAttr ".base_color" -type "float3" 0.018999999 0.0072536562 0.0029259997 ;
	setAttr ".specular" 0.57142859697341919;
	setAttr ".specular_color" -type "float3" 0.50649351 0.50649351 0.50649351 ;
	setAttr ".specular_roughness" 0.36363637447357178;
	setAttr ".subsurface" 0.055944055318832397;
	setAttr ".subsurface_color" -type "float3" 0.012480002 0.078000002 0.052799925 ;
	setAttr ".subsurface_radius" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".sheen" 0.020979020744562149;
	setAttr ".sheen_color" -type "float3" 0.204 0.204 0.104652 ;
	setAttr ".sheen_roughness" 0.034965034574270248;
	setAttr ".coat_color" -type "float3" 0.57191896 1 0.20499998 ;
	setAttr ".coat_roughness" 0;
	setAttr ".coat_IOR" 0;
createNode shadingEngine -n "spikes_SG";
	rename -uid "66BA1DD2-44D7-2818-C10D-21A7D7E7418F";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode place2dTexture -n "spikes_place2dTexture";
	rename -uid "D2B78193-40A7-7936-AA45-0BACD3423B90";
createNode displacementShader -n "spikes_displacementShader";
	rename -uid "BA9A4A26-464A-FBB3-66BC-F593797AD69B";
createNode aiColorCorrect -n "spikes_aiColorCorrect";
	rename -uid "544BE83C-4DFC-666A-EF30-1AB9F9BA3211";
	setAttr ".invert" yes;
	setAttr ".gamma" 7.4000000953674316;
	setAttr ".contrast" 10;
	setAttr ".contrast_pivot" 1;
	setAttr ".exposure" 1.25;
	setAttr ".multiply" -type "float3" 0.003 0.003 0.003 ;
createNode noise -n "spikes_displacement_noise";
	rename -uid "5AEDCD98-4E10-D7AF-31B3-628D93401C81";
	setAttr ".ra" 1;
	setAttr ".fq" 10;
	setAttr ".fr" 3;
	setAttr ".nty" 0;
createNode materialInfo -n "materialInfo1";
	rename -uid "8B34516B-4D9B-9A2C-1196-BBB151F107A5";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "41ED9E5C-4F3C-0E2B-49C3-1A966BAA95E3";
	setAttr -s 3 ".lnk";
	setAttr -s 3 ".slnk";
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 3 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 6 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 2 ".u";
select -ne :defaultRenderingList1;
select -ne :defaultTextureList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "mayaHardware2";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr "spikes_mtl.out" "spikes_SG.ss";
connectAttr "spikes_displacementShader.d" "spikes_SG.ds";
connectAttr "spikes_aiColorCorrect.outr" "spikes_displacementShader.d";
connectAttr "spikes_displacement_noise.ocr" "spikes_aiColorCorrect.inputr";
connectAttr "spikes_displacement_noise.ocr" "spikes_aiColorCorrect.inputg";
connectAttr "spikes_displacement_noise.ocr" "spikes_aiColorCorrect.inputb";
connectAttr "spikes_place2dTexture.o" "spikes_displacement_noise.uv";
connectAttr "spikes_place2dTexture.ofs" "spikes_displacement_noise.fs";
connectAttr "spikes_SG.msg" "materialInfo1.sg";
connectAttr "spikes_mtl.msg" "materialInfo1.m";
connectAttr "spikes_mtl.msg" "materialInfo1.t" -na;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "spikes_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "spikes_SG.message" ":defaultLightSet.message";
connectAttr "spikes_SG.pa" ":renderPartition.st" -na;
connectAttr "spikes_mtl.msg" ":defaultShaderList1.s" -na;
connectAttr "spikes_displacementShader.msg" ":defaultShaderList1.s" -na;
connectAttr "spikes_place2dTexture.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "spikes_aiColorCorrect.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "spikes_displacement_noise.msg" ":defaultTextureList1.tx" -na;
// End of spikes_mtl.ma
