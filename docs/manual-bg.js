"use strict";

function main() {
  // Get A WebGL context
  /** @type {HTMLCanvasElement} */
  const canvas = document.querySelector("#canvas");
  const gl = canvas.getContext("webgl2");
  if (!gl) {
    return;
  }


   // replace in with attribute and out with varying?
  const vs = `#version 300 es
  // an attribute is an input (in) to a vertex shader.
  // It will receive data from a buffer
  in vec4 a_position;

  // all shaders have a main function
  void main() {

    // gl_Position is a special variable a vertex shader
    // is responsible for setting
    gl_Position = a_position;
  }
  `;

  const fs = `#version 300 es
  precision highp float;
  uniform float iTime;
  uniform vec2 iResolution;
  uniform vec2 iMouse;
  uniform vec2 center;
  uniform float zoom_amount;
  uniform int colouring;
  uniform vec3 lp;
  uniform vec3 rp;
  uniform vec3 cmapc;
  uniform int iterParam;
  out vec4 fragColor;
  

  vec3 map(in float t)
  {
      vec3 rgb;
  
      // all colourings
      if (colouring == 1)
      {
          // At sea
          rgb = vec3(
          9.93*pow(t,3.8)*pow((1.-t),0.9),
          12.95*pow(t,2.8)*pow((1.-t),1.3),
          20.67*pow(t,1.8)*pow((1.-t),2.7)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
      else if (colouring == 2)
      {
          // Ice blue
          rgb = vec3(
          70.5*pow(t,4.7)*pow((1.-t),2.6),
          10.18*pow(t,2.8)*pow((1.-t),1.1),
          2.6*pow(t,0.8)*pow((1.-t),0.5)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
      else if (colouring == 3)
      {
          // Yellow and Purple
          rgb = vec3(
          1.68*pow(t,0.2)*pow((1.-t),0.9),
          42.35*pow(t,1.9)*pow((1.-t),4.1),
          4.61*pow(t,1.6)*pow((1.-t),0.8)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
      else if (colouring == 4)
      {
          // Earth
          rgb = vec3(
          5.76*pow(t,0.7)*pow((1.-t),2.8),
          6.49*pow(t,1.3)*pow((1.-t),1.4),
          exp(-9.*pow(t-0.8,2.))
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float(t>=0.));
          //
      }
      else if (colouring == 5)
      {
          // Cyan and Magenta decay
          rgb = vec3(
          2.*exp(-10.*pow(t-0.2,2.))*pow(t,0.6),
          exp(-20.*pow(t-0.7,2.)),
          exp(-5.*pow(t-0.5,2.))
          );
          rgb = vec3(rgb.x,rgb.y,rgb.z);
          //
      }
      else if (colouring == 6)
      {
          // Emergency exit
          rgb = vec3(
          1.68*pow(t,0.2)*pow((1.-t),0.9)*(1.-pow((sin(iTime*2.)+1.)/2.,3.)),
          12.06*pow(t,1.9)*pow((1.-t),1.7),
          1.61*pow(t,1.6)*pow((1.-t),0.8)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
      else if (colouring == 7)
      {
          // Inverted lightness RGB
          rgb = vec3(
          t+0.2*sin(iTime*0.1)-0.2,
          t+0.2*sin(2.+iTime*0.1)-0.2,
          t+0.2*sin(3.+iTime*0.1)-0.2
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.))+float(t>=1.),rgb.y*float((0.<=t)&&(t<=1.))+float(t>=1.),rgb.z*float((0.<=t)&&(t<=1.))+float(t>=1.));
          //
      }
      else if (colouring == 8)
      {
          // Literature
          rgb = vec3(
          7.79*pow(t,1.7)*pow((1.-t),1.3),
          10.18*pow(t,2.8)*pow((1.-t),1.1),
          50.9*pow(t,1.8)*pow((1.-t),5.0)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
          else if (colouring == -1)
      {
          // Literature
          rgb = vec3(
          cmapc.r*pow(t,lp.r)*pow((1.-t),rp.r),
          cmapc.g*pow(t,lp.g)*pow((1.-t),rp.g),
          cmapc.b*pow(t,lp.b)*pow((1.-t),rp.b)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
  
      else
      
      {
          // Default (0)
          rgb = vec3(
          17.484430816275246*pow(t,4.362884336095945)*pow((1.-t),1.1738002744885567),
          5.167710066164584*pow(t,1.33361222833035)*pow((1.-t),1.0584944073735307),
          311.16840825145783*pow(t,4.678644031269574)*pow((1.-t),3.6863406789220625)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
          
  
      return rgb;
  
  }
  
  
  void main( ) {
  
    vec2 uv = vec2(fract(gl_FragCoord.xy / iResolution));
    vec2 fragCoord = uv*iResolution.xy; // this creates an equivalent to ShaderToy's fragCoord variable
    vec2 new_uv = (fragCoord*2. - iResolution.xy)/iResolution.y; // centered

    //vec2 fragCoord = gl_FragCoord.xy;

    
    // fixed
    //vec2 c = vec2(-0.8,0.156);
    vec2 c = vec2(((iMouse.x/iResolution.x)*2.-1.)*2.*zoom_amount*(iResolution.x/(2.*iResolution.y))-center.x, ((-(iMouse.y/iResolution.y)+1.)*2.-1.)*zoom_amount)-center.y;
    //vec2 c = vec2(-0.945, -0.275);
    //vec2 c = vec2(1.008,0.2472);

    vec2 z = new_uv*zoom_amount+center;
    //float gr = 0.65+sin(iTime*0.01)*0.05; //varying circle radii
    //vec2 c = vec2(cos(iTime*0.04), sin(iTime*0.04))*gr; // complex variable c going in circles around origin
    
    /*
        Compute iter iterates of f on the rendered complex plane
        z.x should always be overwritten to real part of f(z),
        z.y should always be overwritten to imaginary part of f(z).
    */

    //int iter = int(iTime*10.);
    int iter = iterParam;


    vec2 check = (z/z)*2.; // constant that's the same size as z, to allow use of lessThan function
    vec2 esc = check*float(iter/2); // escape uv
    
    float p0 = 0.16076937851994388*sin(iTime*0.15+1.9910193300538905);
    float p1 = 0.6000719669940827*sin(iTime*0.03+0.020682468119338715);

    float anim00 = (1.) - (1.*p0*0. + 1.*p1*0.) + (1.*p0*0.*p1*0.);
    float anim01 = (1.*p0*0. + 1.*p1*1.) - (1.*p0*0.*p1*1.);
    float anim10 = (1.*p0*1. + 1.*p1*0.) - (1.*p0*1.*p1*0.);
    float anim11 = (1.*p0*1.*p1*1.);
    
    for (int i=0; i<iter; i++) {

        z = 0.  + anim00 * vec2(
            0.7004145450583352 + ((0.6044396224774313)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.03338250562691791)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.6898107153068738)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.19861207177904805)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((-0.03999132472497102)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))-(0.918134770002353)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((-0.6113938726339854)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))-(-0.555814441022427)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((-0.22873026765475624)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))-(-0.6329455107731279)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.))) + ((0.3282075160769775)*( - 1.0*pow(z.x,0.)*pow(z.y,6.) + 15.0*pow(z.x,2.)*pow(z.y,4.) - 15.0*pow(z.x,4.)*pow(z.y,2.) + 1.0*pow(z.x,6.)*pow(z.y,0.))-(0.5859632630516383)*(6.0*pow(z.x,1.)*pow(z.y,5.) - 20.0*pow(z.x,3.)*pow(z.y,3.) + 6.0*pow(z.x,5.)*pow(z.y,1.))),
            -0.13641582779589445 + ((0.03338250562691791)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.6044396224774313)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.19861207177904805)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.6898107153068738)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((0.918134770002353)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))+(-0.03999132472497102)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((-0.555814441022427)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))+(-0.6113938726339854)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((-0.6329455107731279)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))+(-0.22873026765475624)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.))) + ((0.5859632630516383)*( - 1.0*pow(z.x,0.)*pow(z.y,6.) + 15.0*pow(z.x,2.)*pow(z.y,4.) - 15.0*pow(z.x,4.)*pow(z.y,2.) + 1.0*pow(z.x,6.)*pow(z.y,0.))+(0.3282075160769775)*(6.0*pow(z.x,1.)*pow(z.y,5.) - 20.0*pow(z.x,3.)*pow(z.y,3.) + 6.0*pow(z.x,5.)*pow(z.y,1.)))
        ) + anim01 * vec2(
            -0.9212962546620287 + ((0.7197372989973891)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(-0.7253114552760711)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.38079875716475065)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.43073975682349785)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((0.5774237897322967)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))-(-0.42373979220231184)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((0.685916735398818)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))-(-0.8064202962615716)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((-0.7780927319082098)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))-(0.20090763640248555)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.))) + ((0.6467518184170615)*( - 1.0*pow(z.x,0.)*pow(z.y,6.) + 15.0*pow(z.x,2.)*pow(z.y,4.) - 15.0*pow(z.x,4.)*pow(z.y,2.) + 1.0*pow(z.x,6.)*pow(z.y,0.))-(0.6063804191332658)*(6.0*pow(z.x,1.)*pow(z.y,5.) - 20.0*pow(z.x,3.)*pow(z.y,3.) + 6.0*pow(z.x,5.)*pow(z.y,1.))),
            -0.03196626043505746 + ((-0.7253114552760711)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.7197372989973891)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.43073975682349785)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(0.38079875716475065)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((-0.42373979220231184)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))+(0.5774237897322967)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((-0.8064202962615716)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))+(0.685916735398818)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((0.20090763640248555)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))+(-0.7780927319082098)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.))) + ((0.6063804191332658)*( - 1.0*pow(z.x,0.)*pow(z.y,6.) + 15.0*pow(z.x,2.)*pow(z.y,4.) - 15.0*pow(z.x,4.)*pow(z.y,2.) + 1.0*pow(z.x,6.)*pow(z.y,0.))+(0.6467518184170615)*(6.0*pow(z.x,1.)*pow(z.y,5.) - 20.0*pow(z.x,3.)*pow(z.y,3.) + 6.0*pow(z.x,5.)*pow(z.y,1.)))
        ) + anim10 * vec2(
            -0.13393070297779563 + ((-0.33791708359440564)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.5369388645388715)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.05197607922591008)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.6825063897295924)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((-0.41208738021929747)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))-(-0.9908542924045498)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((0.429477032843933)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))-(-0.3578056991213483)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((-0.9588773874023786)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))-(-0.20731027858070172)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.))) + ((-0.6482861711537331)*( - 1.0*pow(z.x,0.)*pow(z.y,6.) + 15.0*pow(z.x,2.)*pow(z.y,4.) - 15.0*pow(z.x,4.)*pow(z.y,2.) + 1.0*pow(z.x,6.)*pow(z.y,0.))-(0.0030994464877027728)*(6.0*pow(z.x,1.)*pow(z.y,5.) - 20.0*pow(z.x,3.)*pow(z.y,3.) + 6.0*pow(z.x,5.)*pow(z.y,1.))),
            -0.10843265710543726 + ((0.5369388645388715)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(-0.33791708359440564)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.6825063897295924)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(0.05197607922591008)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((-0.9908542924045498)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))+(-0.41208738021929747)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((-0.3578056991213483)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))+(0.429477032843933)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((-0.20731027858070172)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))+(-0.9588773874023786)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.))) + ((0.0030994464877027728)*( - 1.0*pow(z.x,0.)*pow(z.y,6.) + 15.0*pow(z.x,2.)*pow(z.y,4.) - 15.0*pow(z.x,4.)*pow(z.y,2.) + 1.0*pow(z.x,6.)*pow(z.y,0.))+(-0.6482861711537331)*(6.0*pow(z.x,1.)*pow(z.y,5.) - 20.0*pow(z.x,3.)*pow(z.y,3.) + 6.0*pow(z.x,5.)*pow(z.y,1.)))
        ) + anim11 * vec2(
            0.276539474407431 + ((-0.45280740645504736)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(-0.8518265012766428)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.07662035411933443)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.04287108415843499)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((-0.4712850652746936)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))-(-0.6577659600199899)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((-0.7068887783903062)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))-(0.9985599993361189)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((-0.4752026936719551)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))-(0.5566525703066789)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.))) + ((-0.5763442858088728)*( - 1.0*pow(z.x,0.)*pow(z.y,6.) + 15.0*pow(z.x,2.)*pow(z.y,4.) - 15.0*pow(z.x,4.)*pow(z.y,2.) + 1.0*pow(z.x,6.)*pow(z.y,0.))-(0.8836019570486509)*(6.0*pow(z.x,1.)*pow(z.y,5.) - 20.0*pow(z.x,3.)*pow(z.y,3.) + 6.0*pow(z.x,5.)*pow(z.y,1.))),
            0.26146608979581787 + ((-0.8518265012766428)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(-0.45280740645504736)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.04287108415843499)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(0.07662035411933443)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((-0.6577659600199899)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))+(-0.4712850652746936)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((0.9985599993361189)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))+(-0.7068887783903062)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((0.5566525703066789)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))+(-0.4752026936719551)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.))) + ((0.8836019570486509)*( - 1.0*pow(z.x,0.)*pow(z.y,6.) + 15.0*pow(z.x,2.)*pow(z.y,4.) - 15.0*pow(z.x,4.)*pow(z.y,2.) + 1.0*pow(z.x,6.)*pow(z.y,0.))+(-0.5763442858088728)*(6.0*pow(z.x,1.)*pow(z.y,5.) - 20.0*pow(z.x,3.)*pow(z.y,3.) + 6.0*pow(z.x,5.)*pow(z.y,1.)))
        );


        esc -= vec2(lessThan(z,check)); // does not work as intended as big values aren't "bigger", just undefined
    }

    esc /= float(iter); // esc values are between 0 and iter, so they need to be normalized

    float zmod = sqrt(z.x*z.x + z.y*z.y);
    float angle = atan(z.y/z.x);
    
    // smooth colouring using modified Bernstein equations
    float t = length(esc);
    vec3 RGB = map(t);
    //vec3 RGB = vec3(zmod, angle, angle);

    // iMouse.x/iResolution.x //
    // iMouse.y/iResolution.y //
    // how close the mouse is to the right / bottom edge of the screen between [0,1]

    // RGB = RGB + hsl2rgb(vec3(angle, 0.3, zmod));

    fragColor = vec4(RGB, 1.0);


}
  `;

  // setup GLSL program
  const program = webglUtils.createProgramFromSources(gl, [vs, fs]);

  // look up where the vertex data needs to go.
  const positionAttributeLocation = gl.getAttribLocation(program, "a_position");

  // look up uniform locations
  const resolutionLocation = gl.getUniformLocation(program, "iResolution");
  const mouseLocation = gl.getUniformLocation(program, "iMouse");
  const timeLocation = gl.getUniformLocation(program, "iTime");
  const centerLocation = gl.getUniformLocation(program, "center");
  const zoomamountLocation = gl.getUniformLocation(program, "zoom_amount");
  const iterParamLocation = gl.getUniformLocation(program, "iterParam");
  
  const colouringLocation = gl.getUniformLocation(program, "colouring");
  const cmapcLocation = gl.getUniformLocation(program, "cmapc");
  const lpLocation = gl.getUniformLocation(program, "lp");
  const rpLocation = gl.getUniformLocation(program, "rp");
  
  
  
  

  // Create a vertex array object (attribute state)
  const vao = gl.createVertexArray();

  // and make it the one we're currently working with
  gl.bindVertexArray(vao);

  // Create a buffer to put three 2d clip space points in
  const positionBuffer = gl.createBuffer();

  // Bind it to ARRAY_BUFFER (think of it as ARRAY_BUFFER = positionBuffer)
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

  // fill it with a 2 triangles that cover clip space
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
    -1, -1,  // first triangle
     1, -1,
    -1,  1,
    -1,  1,  // second triangle
     1, -1,
     1,  1,
  ]), gl.STATIC_DRAW);

  // Turn on the attribute
  gl.enableVertexAttribArray(positionAttributeLocation);

  // Tell the attribute how to get data out of positionBuffer (ARRAY_BUFFER)
  gl.vertexAttribPointer(
      positionAttributeLocation,
      2,          // 2 components per iteration
      gl.FLOAT,   // the data is 32bit floats
      false,      // don't normalize the data
      0,          // 0 = move forward size * sizeof(type) each iteration to get the next position
      0,          // start at the beginning of the buffer
  );

  let mouseX = 0;
  let mouseY = 0;

  function setMousePosition(e) {
    const rect = canvas.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = rect.height - (e.clientY - rect.top) - 1;  // bottom is 0 in WebGL
  }

  canvas.addEventListener('mousemove', setMousePosition);
  canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
  }, {passive: false});
  canvas.addEventListener('touchmove', (e) => {
    e.preventDefault();
    setMousePosition(e.touches[0]);
  }, {passive: false});

  function render(time) {
    time *= 0.001;  // convert to seconds

    webglUtils.resizeCanvasToDisplaySize(gl.canvas);

    // Tell WebGL how to convert from clip space to pixels
    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

    // Tell it to use our program (pair of shaders)
    gl.useProgram(program);

    // Bind the attribute/buffer set we want.
    gl.bindVertexArray(vao);

    gl.uniform2f(resolutionLocation, gl.canvas.width, gl.canvas.height);
    gl.uniform2f(mouseLocation, mouseX, mouseY);
    gl.uniform2f(centerLocation, 0,0);
    gl.uniform1f(timeLocation, time);
    gl.uniform1i(iterParamLocation, 50);
    gl.uniform1f(zoomamountLocation, 1.2);
    gl.uniform1i(colouringLocation, 7);
    gl.uniform3f(cmapcLocation, 1.0,1.0,1.0);
    gl.uniform3f(lpLocation, 1.0,1.0,1.0);
    gl.uniform3f(rpLocation, 1.0,1.0,1.0);
    
    

    gl.drawArrays(
        gl.TRIANGLES,
        0,     // offset
        6,     // num vertices to process
    );

    requestAnimationFrame(render);
    
  }
  
  requestAnimationFrame(render);

  


}


main();
