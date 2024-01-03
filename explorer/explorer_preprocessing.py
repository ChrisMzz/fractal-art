import numpy as np


def lcm(x, y):
    return (x*y)//np.gcd(x, y)

def binomial_coefficient(n,k):
    return np.math.factorial(n)/(np.math.factorial(k)*np.math.factorial(n-k))

def loop_over_positions(shape, k=0): # all positions
        if k == len(shape)-1: 
            temp_list = []
            for j in range(shape[-1]): 
                temp = list(shape)
                temp[-1] = j
                temp_list.append(tuple(temp))
            return temp_list
        temp_list = []
        for j in range(shape[k]):
            temp = list(shape)
            temp[k] = j
            temp_list += loop_over_positions(tuple(temp), k+1)
        return temp_list
    
def hypercorners(shape):
    return [tuple((np.array(shape)-1)*np.array(pos)) for pos in loop_over_positions(tuple(len(shape)*[2]))]
    




class SymmetricGroup :

    def __init__(self, n):
        self.group = []
        for i in range(1, n+1):
            self.element_gen(self.group, [str(i)], n)
            
    def element_gen(self, group, qlist, n):
        perm = list(range(1, n+1))
        for i in qlist:
            perm.remove(int(i))
        if perm != []:
            for i in perm:
                self.element_gen(group, qlist + [str(i)], n)
        else:
            self.group.append(qlist)

    def __iter__(self):
        for sigma in self.group:
            yield sigma

    def signature(self, perm):
        s = 1
        qlist = list(perm)
        for i in range(1, len(perm)+1):
            while int(qlist[i-1]) != i:
                a = int(qlist[i-1])
                b = int(qlist[a-1])
                qlist[a-1] = str(a)
                qlist[i-1] = str(b)
                s *= -1
        return s

    def compute_orbits(self, perm):
        qlist = list(perm)
        orbits = []
        for i in range(1, len(perm)+1):
            orbit = []
            b = 0
            while int(qlist[i-1]) != i:
                if b != 0:
                    orbit.remove(b)
                a = int(qlist[i-1])
                b = int(qlist[a-1])
                qlist[a-1] = str(a)
                qlist[i-1] = str(b)
                orbit.append(int(a))
                orbit.append(int(b))
            if orbit != []:
                orbits.append(orbit)
        return orbits

    def orbits(self, perm):
        orbits = ""
        for orbit in self.compute_orbits(perm):
            orbits += str(tuple(orbit))
        return orbits
    
    
    def order(self, perm):
        orbit_lens = []       
        for orbit in self.compute_orbits(perm):
            orbit_lens.append(len(orbit))
        order = 1
        for i in orbit_lens:
            order = lcm(order, i)
        return order
        
            
    def to_string(self, perm):
        query = ""
        for num in perm:
            query += str(num) + " "
        return query


class BinomialCoeff : 
    def __init__(self,n,p):
        self.n = n
        self.p = p
        self.card = (np.math.factorial(n)/(np.math.factorial(n-p)*np.math.factorial(p)))
        self.elements = []
        self.build()
        
    def __str__(self):
        temp = ""
        for element in self.elements:
            temp += str(element) + "\n"
        return temp
    
    def __iter__(self):
        for element in self.elements:
            yield element
    
    def build(self):
        for sigma in SymmetricGroup(self.n):
            pot = [int(el) for el in sigma]
            while len(pot) != self.p:
                pot.pop(-1)
            if sorted(pot) not in self.elements:
                self.elements.append(sorted(pot))
                
def define_parameter(pos):
    N = len(pos)
    p = [f'p{k}' for k in range(N)]
    pos_list = list(pos)
    n = N
    while '1' in pos_list: n -= 1; pos_list.remove('1')
    res = ''
    parity = 1
    for step, k in enumerate(range(N-n,N+1)):
        temp = f'{" - " if parity == -1 else " + " if step > 0 else ""}('
        for comb in BinomialCoeff(N,k): 
            temp += f'1.{"".join([f"*{p[c-1]}*{pos[c-1]}" for c in comb])} + '
        parity *= -1
        res += temp[:-3] + ')'
    return res



class FrctlFile:
    def __init__(self, arr, metadata):
        self.arr = arr
        self.metadata = metadata
        
    def frctl(self):
        if len(self.arr.shape) == 2: return CustomFrctl(self.arr, self.metadata)
        if len(self.arr.shape) > 2:  return CustomFrctlAnim(self.arr, self.metadata)
        
        


class CustomFrctl(FrctlFile):
    def __init__(self, arr, metadata):
        self.arr = arr
        self.cmap_dict = metadata["cmap_dict"]
        self.ordertxt = metadata["ordertxt"]
    
    
    def parse_cmap(self):
        rlp, rrp, glp, grp, blp, brp = [float(self.cmap_dict[key]) for key in 
                                        ("rlp", "rrp", "glp", "grp", "blp", 'brp')]
        rc, gc, bc = [float(self.cmap_dict[key]) for key in ("rc","gc","bc")]
        R, G, B = (rc, rlp, rrp), (gc, glp, grp), (bc, blp, brp)
        temp_param = []
        for canal in self.ordertxt:
            if canal == "r" or canal == "R": temp_param.append(R)
            if canal == "g" or canal == "G": temp_param.append(G)
            if canal == "b" or canal == "B": temp_param.append(B)
        (rc, rlp, rrp), (gc, glp, grp), (bc, blp, brp) = temp_param
        return f"""
    {'{'}
        // Default (0)
        rgb = vec3(
        {rc}*pow(t,{rlp})*pow((1.-t),{rrp}),
        {gc}*pow(t,{glp})*pow((1.-t),{grp}),
        {bc}*pow(t,{blp})*pow((1.-t),{brp})
        );
        rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
        //
    {'}'}
        """
    
    def parse_z(self):
        o = self.arr.shape[-1]
        re = f"{self.arr[0,0]}"
        im = f"{self.arr[1,0]}"
        for k in range(1,o):
            re_k, im_k = self.compute_newton(self.arr[0,k]+1j*self.arr[1,k], k)
            re += f" + {re_k}"
            im += f" + {im_k}"
        return f"""z = vec2(
            {re},
            {im}
        );"""
    
    def compute_newton(self, coefficient, p):
        """Get separation of real and imaginary parts of c*z**p formatted for GLSL frag shader.

            coefficient : complex
            p : int
        """
        re = ""
        im = ""
        a,b = coefficient.real, coefficient.imag
        for k in range(p+1):
            current = f"{binomial_coefficient(p,k)}*pow(z.x,{k}.)*pow(z.y,{p-k}.)"
            if (p-k)%4 == 0: re += [" + ",""][int(re=="")] + current
            elif (p-k)%4 == 1: im += [" + ",""][int(im=="")] + current
            elif (p-k)%4 == 2: re += f" - {current}"
            elif (p-k)%4 == 3: im += f" - {current}"
            else: raise ValueError(f"{p-k} is not an integer.")
        return  f"(({a})*({re})-({b})*({im}))", f"(({b})*({re})+({a})*({im}))"
            
    def parse(self):
        return """#version 330 core
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
    """+ self.parse_cmap() + """

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
    //int iter = iterParam;


    vec2 check = (z/z)*2.; // constant that's the same size as z, to allow use of lessThan function
    vec2 esc = check*iter/2; // escape uv
    
    for (int i=0; i<iter; i++) {

        """ + self.parse_z() + """


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


}"""


class CustomFrctlAnim(FrctlFile):
    def __init__(self, arr, metadata):
        self.arr = arr
        self.cmap_dict = metadata["cmap_dict"]
        self.ordertxt = metadata["ordertxt"]
    
    
    def parse_cmap(self):
        rlp, rrp, glp, grp, blp, brp = [float(self.cmap_dict[key]) for key in 
                                        ("rlp", "rrp", "glp", "grp", "blp", 'brp')]
        rc, gc, bc = [float(self.cmap_dict[key]) for key in ("rc","gc","bc")]
        R, G, B = (rc, rlp, rrp), (gc, glp, grp), (bc, blp, brp)
        temp_param = []
        for canal in self.ordertxt:
            if canal == "r" or canal == "R": temp_param.append(R)
            if canal == "g" or canal == "G": temp_param.append(G)
            if canal == "b" or canal == "B": temp_param.append(B)
        (rc, rlp, rrp), (gc, glp, grp), (bc, blp, brp) = temp_param
        return f"""
    {'{'}
        // Default (0)
        rgb = vec3(
        {rc}*pow(t,{rlp})*pow((1.-t),{rrp}),
        {gc}*pow(t,{glp})*pow((1.-t),{grp}),
        {bc}*pow(t,{blp})*pow((1.-t),{brp})
        );
        rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
        //
    {'}'}
        """
    
    def parse_z(self,pos):
        o = self.arr.shape[-1]
        re = f"{self.arr[pos][0,0]}"
        im = f"{self.arr[pos][1,0]}"
        for k in range(1,o):
            re_k, im_k = self.compute_newton(self.arr[pos][0,k]+1j*self.arr[pos][1,k], k)
            re += f" + {re_k}"
            im += f" + {im_k}"
        return f""" + anim{''.join(map(str,tuple(np.array(np.array(pos)>0,dtype=int))))} * vec2(
            {re},
            {im}
        )"""
        
    
    
    def compute_newton(self, coefficient, p):
        """Get separation of real and imaginary parts of c*z**p formatted for GLSL frag shader.

            coefficient : complex
            p : int
        """
        re = ""
        im = ""
        a,b = coefficient.real, coefficient.imag
        for k in range(p+1):
            current = f"{binomial_coefficient(p,k)}*pow(z.x,{k}.)*pow(z.y,{p-k}.)"
            if (p-k)%4 == 0: re += [" + ",""][int(re=="")] + current
            elif (p-k)%4 == 1: im += [" + ",""][int(im=="")] + current
            elif (p-k)%4 == 2: re += f" - {current}"
            elif (p-k)%4 == 3: im += f" - {current}"
            else: raise ValueError(f"{p-k} is not an integer.")
        return  f"(({a})*({re})-({b})*({im}))", f"(({b})*({re})+({a})*({im}))"
            
    def parse(self):
        return """#version 330 core
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
    """+ self.parse_cmap() + """

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
    
    // Note : only need N parameters to completely parametrically describe a N-dimensional cuboids
    // Example in 2D for a quadrilateral ABCD, using parameters t0 and t1 : 
    // (1 - t0 - t1 + t0t1)A + (t0 - t0t1)B + (t1 -t0t1)C + (t0t1)D
    // Example in 3D for a cuboid ABCDEFGH, using parameters t0, t1 and t2 : 
    // (1 - t0 - t1 - t2 + t0t1 + t0t2 + t1t2 - t0t1t2) A + (t0 - (t0t1+t0t2) + t0t1t2 ) B + (t1 - (t0t1 + t1t2) + t0t1t2) C + (t2 - (t0t2 + t1t2) + t0t1t2)E + (t0t1 - t0t1t2) D + (t0t2 - t0t1t2) F + (t1t2 - t0t1t2) G + (t0t1t2)H
    // We can actually generalise this formula using binomial coefficients over an arbitrary N

    """ + '    '.join([f"float p{k} = {np.random.rand()}*sin(iTime*0.02+{np.random.rand()*4});\n" for k in range(len(self.arr.shape[:-2]))]) + '\n    ' + '\n    '.join([f"float anim{''.join(map(str, tuple(np.array(np.array(pos)>0,dtype=int))))} = {define_parameter(''.join(map(str, tuple(np.array(np.array(pos)>0,dtype=int)))))};" for pos in hypercorners(self.arr.shape[:-2])]) + """
    
    /*
        Compute iter iterates of f on the rendered complex plane
        z.x should always be overwritten to real part of f(z),
        z.y should always be overwritten to imaginary part of f(z).
    */

    //int iter = int(iTime*10.);
    int iter = iterParam;


    vec2 check = (z/z)*2.; // constant that's the same size as z, to allow use of lessThan function
    vec2 esc = check*iter/2; // escape uv
    
    for (int i=0; i<iter; i++) {

        z = 0. """ + ''.join([self.parse_z(pos) for pos in hypercorners(self.arr.shape[:-2])]) + """;


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


}"""





if __name__ == "__main__":
    
    test = CustomFrctl(np.array([[0.285,0.0,1.0],[0.01,0.0,0.0]]), {"cmap_dict":{
        "rc":8.5, "gc":15, "bc":9,
        "rlp":3, "glp":2, "blp":1, "rrp":1, "grp":2, "brp":3
    }})
    
    print(test.parse())


