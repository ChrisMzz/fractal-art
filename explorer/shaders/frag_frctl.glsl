#version 330 core
in vec2 uv;
uniform float iTime;
uniform vec2 iResolution;
uniform vec2 iMouse;
uniform vec2 center;
uniform float zoom_amount;
uniform int colouring;
uniform vec3 lp;
uniform vec3 rp;
uniform vec3 cmapc;
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
        2*exp(-10.*pow(t-0.2,2.))*pow(t,0.6),
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
        1.68*pow(t,0.2)*pow((1.-t),0.9)*(1-pow((sin(iTime*2.)+1.)/2.,3.)),
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
        24.56359017676485*pow(t,3.3169403792176397)*pow((1.-t),1.6889826104224315),
        127.54740076996872*pow(t,2.667304666185057)*pow((1.-t),4.755706243849141),
        4.091783693113925*pow(t,2.9861728315930662)*pow((1.-t),0.4875150140722738)
        );
        rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
        //
    }
        

    return rgb;

}


vec3 hsl2rgb( in vec3 c )
{
    vec3 rgb = clamp( abs(mod(c.x*6.0+vec3(0.0,4.0,2.0),6.0)-3.0)-1.0, 0.0, 1.0 );

    return c.z + c.y * (rgb-0.5)*(1.0-abs(2.0*c.z-1.0));
}

void main( )
{
    vec2 fragCoord = uv*iResolution.xy; // this creates an equivalent to ShaderToy's fragCoord variable
    vec2 new_uv = (fragCoord*2. - iResolution.xy)/iResolution.y; // centered


    vec2 z = new_uv*zoom_amount+center;
    //float gr = 0.65+sin(iTime*0.01)*0.05; //varying circle radii
    //vec2 c = vec2(cos(iTime*0.04), sin(iTime*0.04))*gr; // complex variable c going in circles around origin
    
    // fixed
    vec2 c = vec2(0.,0.);
    //vec2 c = vec2(((iMouse.x/iResolution.x)*2.-1.)*2*zoom_amount*(iResolution.x/(2.*iResolution.y))-center.x, ((-(iMouse.y/iResolution.y)+1.)*2.-1.)*zoom_amount)-center.y;

    /*
        Compute iter iterates of f on the rendered complex plane
        z.x should always be overwritten to real part of f(z),
        z.y should always be overwritten to imaginary part of f(z).
    */

    int iter = int(iTime*10.);
    //int iter = 200;


    vec2 check = (z/z)*2.; // constant that's the same size as z, to allow use of lessThan function
    vec2 esc = check*iter/2; // escape uv
    
    for (int i=0; i<iter; i++) {

        z = vec2(
            -0.07379362864059802 + ((-0.6614655625997423)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.6920684473508174)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.37009102368059543)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.9141592499437421)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((-0.25203773537241325)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))-(0.9965888843846091)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((0.24681331392385975)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))-(-0.7324248440055514)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((-0.39427866232531694)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))-(0.5895258772328513)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.))) + ((0.4102157127783519)*( - 1.0*pow(z.x,0.)*pow(z.y,6.) + 15.0*pow(z.x,2.)*pow(z.y,4.) - 15.0*pow(z.x,4.)*pow(z.y,2.) + 1.0*pow(z.x,6.)*pow(z.y,0.))-(-0.26865292820930686)*(6.0*pow(z.x,1.)*pow(z.y,5.) - 20.0*pow(z.x,3.)*pow(z.y,3.) + 6.0*pow(z.x,5.)*pow(z.y,1.))),
            0.15737685619193043 + ((0.6920684473508174)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(-0.6614655625997423)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.9141592499437421)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(0.37009102368059543)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((0.9965888843846091)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))+(-0.25203773537241325)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((-0.7324248440055514)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))+(0.24681331392385975)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((0.5895258772328513)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))+(-0.39427866232531694)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.))) + ((-0.26865292820930686)*( - 1.0*pow(z.x,0.)*pow(z.y,6.) + 15.0*pow(z.x,2.)*pow(z.y,4.) - 15.0*pow(z.x,4.)*pow(z.y,2.) + 1.0*pow(z.x,6.)*pow(z.y,0.))+(0.4102157127783519)*(6.0*pow(z.x,1.)*pow(z.y,5.) - 20.0*pow(z.x,3.)*pow(z.y,3.) + 6.0*pow(z.x,5.)*pow(z.y,1.)))
        );


        esc -= vec2(lessThan(z,check)); // does not work as intended as big values aren't "bigger", just undefined
    }

    esc /= iter; // esc values are between 0 and iter, so they need to be normalized

    float zmod = sqrt(z.x*z.x + z.y*z.y);
    float angle = atan(z.y/z.x);
    
    // smooth colouring using modified Bernstein equations
    float t = length(esc);
    vec3 RGB = map(t);

    // iMouse.x/iResolution.x //
    // iMouse.y/iResolution.y //
    // how close the mouse is to the right / bottom edge of the screen between [0,1]

    // RGB = RGB + hsl2rgb(vec3(angle, 0.3, zmod));

    fragColor = vec4(RGB, 1.0);


}